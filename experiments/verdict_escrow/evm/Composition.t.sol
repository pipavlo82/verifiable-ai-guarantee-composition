// SPDX-License-Identifier: MIT
pragma solidity ^0.8.23;
import "forge-std/Test.sol";
import {VerdictGatedEscrow,IERC20} from "../vendor/invinoveritas/integrations/verdict-escrow/src/VerdictGatedEscrow.sol";
contract LabToken {
    mapping(address=>uint256) public balanceOf;
    mapping(address=>mapping(address=>uint256)) public allowance;
    uint256 public behavior;
    function setBehavior(uint256 b) external {behavior=b;}
    function mint(address a,uint256 v) external {balanceOf[a]+=v;}
    function approve(address a,uint256 v) external returns(bool){allowance[msg.sender][a]=v;return true;}
    function transferFrom(address a,address b,uint256 v) external returns(bool){require(allowance[a][msg.sender]>=v && balanceOf[a]>=v);allowance[a][msg.sender]-=v;balanceOf[a]-=v;balanceOf[b]+=v;return true;}
    function transfer(address a,uint256 v) external returns(bool){if(behavior==1)return false;if(behavior==2)return true;require(balanceOf[msg.sender]>=v);balanceOf[msg.sender]-=v;balanceOf[a]+=v;return true;}
}
contract CompositionTest is Test {
    LabToken t;VerdictGatedEscrow e;VerdictGatedEscrow other;
    address constant PAYER=address(0xA11CE);address constant PAYEE=address(0xB0B);
    bytes32 constant SALT=bytes32("joint-lab");
    struct Wire {bytes32 request;bytes32 policy;bytes32 decision;bytes32 r;bytes32 s;uint256 nonce;bool admitted;uint256 status;}
    function py(string[] memory args) internal returns(bytes memory){
        string[] memory c=new string[](args.length+2);c[0]=vm.envString("LAB_PYTHON");c[1]="bridge.py";
        for(uint i;i<args.length;i++)c[i+2]=args[i];return vm.ffi(c);
    }
    function setUp() public {
        vm.chainId(8453);vm.warp(1000);t=new LabToken();string[] memory a=new string[](1);a[0]="pubkey";bytes32 key=bytes32(py(a));
        e=new VerdictGatedEscrow(IERC20(address(t)),key);other=new VerdictGatedEscrow(IERC20(address(t)),key);t.mint(PAYER,100e6);
        vm.startPrank(PAYER);t.approve(address(e),type(uint256).max);t.approve(address(other),type(uint256).max);vm.stopPrank();
    }
    function wire(string memory name,uint256 targetId) internal returns(Wire memory w){
        string[] memory a=new string[](7);a[0]="vector";a[1]=name;a[2]=vm.toString(address(e));a[3]=vm.toString(address(t));a[4]=vm.toString(e.escrowId(PAYER,SALT));a[5]=vm.toString(address(other));a[6]=vm.toString(targetId);
        w=abi.decode(py(a),(Wire));
    }
    function eq(string memory a,string memory b) internal pure returns(bool){return keccak256(bytes(a))==keccak256(bytes(b));}
    function one(string memory name) internal {
        VerdictGatedEscrow target=eq(name,"C_other_escrow")?other:e;
        bytes32 salt=eq(name,"G_other_payment")?bytes32("other-job"):SALT;
        uint256 id=target.escrowId(PAYER,salt);Wire memory w=wire(name,id);
        address recipient=eq(name,"E_other_recipient")?address(0xDEAD):PAYEE;
        uint256 amount=eq(name,"F_other_amount")?2e6:1e6;
        vm.prank(PAYER);target.fund(salt,recipient,amount,w.request,w.policy,1,2000);
        bytes memory sig=abi.encodePacked(w.r,w.s);
        if(eq(name,"D_other_chain"))vm.chainId(8454);
        if(eq(name,"I_expired")||eq(name,"expired_after_signing"))vm.warp(2000);
        if(eq(name,"H_replay")||eq(name,"O_duplicate")){target.release(id,w.nonce,w.decision,sig);t.mint(address(target),amount);}
        if(eq(name,"refund_then_release")){vm.warp(2000);target.refund(id);t.mint(address(target),amount);}
        if(eq(name,"false_returning_token"))t.setBehavior(1);
        if(eq(name,"lying_token"))t.setBehavior(2);
        uint256 beforeBalance=t.balanceOf(recipient);uint256 beforeGas=gasleft();
        (bool ok,bytes memory ret)=address(target).call(abi.encodeCall(target.release,(id,w.nonce,w.decision,sig)));
        uint256 used=beforeGas-gasleft();uint256 delta=t.balanceOf(recipient)-beforeBalance;
        bool mustReject=eq(name,"C_other_escrow")||eq(name,"D_other_chain")||eq(name,"G_other_payment")||eq(name,"H_replay")||eq(name,"O_duplicate")||eq(name,"J_unauthorized")||eq(name,"false_returning_token")||eq(name,"high_s")||eq(name,"invalid_signature")||eq(name,"negated_s")||eq(name,"refund_then_release");
        assertEq(ok,!mustReject,string.concat("unexpected chain behavior: ",name));
        if(ok&&!eq(name,"lying_token"))assertEq(delta,amount,"observed token movement");else assertEq(delta,0,"no token movement");
        if(eq(name,"positive")){assertTrue(w.admitted);assertEq(target.releaseDigest(id,w.nonce,w.decision),sha256(abi.encode(target.DOMAIN_TAG(),uint256(8453),address(e),address(e),id,w.nonce,uint256(1),w.request,w.policy,uint256(1),w.decision)));}
        string memory obj=name;vm.serializeString(obj,"name",name);vm.serializeBool(obj,"onchain_success",ok);vm.serializeBool(obj,"offchain_admitted",w.admitted);vm.serializeUint(obj,"offchain_status_code",w.status);vm.serializeUint(obj,"release_call_gas",used);vm.serializeUint(obj,"recipient_delta",delta);vm.serializeUint(obj,"amount",amount);vm.serializeAddress(obj,"escrow",address(target));vm.serializeAddress(obj,"recipient",recipient);vm.serializeBytes(obj,"return_data",ret);
        (,,,,,,,VerdictGatedEscrow.State state)=target.escrows(id);string memory data=vm.serializeUint(obj,"state",uint256(state));
        vm.writeJson(data,string.concat(vm.envString("LAB_EVIDENCE_DIR"),"/",name,"-evm.json"));
    }
    function test_all_vectors() public {
        string[31] memory names=["positive","A_wrong_scope","B_missing_obligation","C_other_escrow","D_other_chain","E_other_recipient","F_other_amount","G_other_payment","H_replay","I_expired","J_unauthorized","J_revoked","K_evidence_digest","L_no_contract","M_unverified_field","N_self_judgment","O_duplicate","P_incorrect_authorization","Q_record_tamper","R_other_profile","nonce_reused_other_job","changed_scenario_digest","missing_profile","expired_after_signing","revoked_after_signing","false_returning_token","high_s","invalid_signature","refund_then_release","lying_token","negated_s"];
        for(uint256 i;i<names.length;i++){uint256 snap=vm.snapshotState();one(names[i]);assertTrue(vm.revertToState(snap));}
    }
    function test_refund_deadline_is_not_verdict_expiry() public {one("I_expired");}
    function test_document_recipient_is_not_enforced() public {one("E_other_recipient");}
    function test_document_amount_is_not_enforced() public {one("F_other_amount");}
    function test_signature_is_not_semantic_authorization() public {one("A_wrong_scope");}
    function test_success_is_not_payment_for_arbitrary_token() public {one("lying_token");}
    function test_nonce_is_not_global_across_payments() public {
        uint256 paid;
        for(uint256 i;i<2;i++){
            bytes32 salt=bytes32(i+100);uint256 id=e.escrowId(PAYER,salt);
            string[] memory a=new string[](7);a[0]="vector";a[1]=i==0?"nonce_first_payment":"nonce_second_payment";a[2]=vm.toString(address(e));a[3]=vm.toString(address(t));a[4]=vm.toString(id);a[5]=vm.toString(address(other));a[6]=vm.toString(id);
            Wire memory w=abi.decode(py(a),(Wire));assertEq(w.nonce,7);
            vm.prank(PAYER);e.fund(salt,PAYEE,1e6,w.request,w.policy,1,2000);
            e.release(id,w.nonce,w.decision,abi.encodePacked(w.r,w.s));paid++;
        }
        assertEq(t.balanceOf(PAYEE),2e6);
        string memory obj="two-payments";vm.serializeUint(obj,"shared_submission_id",7);vm.serializeUint(obj,"paid_escrows",paid);string memory data=vm.serializeUint(obj,"recipient_delta",t.balanceOf(PAYEE));vm.writeJson(data,string.concat(vm.envString("LAB_EVIDENCE_DIR"),"/two-payments.json"));
    }
}
