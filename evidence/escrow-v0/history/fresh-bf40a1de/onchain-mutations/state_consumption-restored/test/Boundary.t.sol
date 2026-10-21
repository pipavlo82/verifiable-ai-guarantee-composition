// SPDX-License-Identifier: MIT
pragma solidity ^0.8.23;
import "forge-std/Test.sol";
import {VerdictGatedEscrow,IERC20} from "../src/VerdictGatedEscrow.sol";
contract MToken {mapping(address=>uint256) public balanceOf;function mint(address a,uint256 n) external{balanceOf[a]+=n;}function transferFrom(address a,address b,uint256 n) external returns(bool){require(balanceOf[a]>=n);balanceOf[a]-=n;balanceOf[b]+=n;return true;}function transfer(address a,uint256 n) external returns(bool){require(balanceOf[msg.sender]>=n);balanceOf[msg.sender]-=n;balanceOf[a]+=n;return true;}}
contract BoundaryMutationTest is Test {
 MToken t;VerdictGatedEscrow e;VerdictGatedEscrow other;address payer=address(0xA11CE);address payee=address(0xB0B);bytes32 salt=bytes32("joint-lab");
 struct Wire {bytes32 request;bytes32 policy;bytes32 decision;bytes32 r;bytes32 s;uint256 nonce;bool admitted;uint256 status;}
 function py(string[] memory a) internal returns(bytes memory){string[] memory c=new string[](a.length+2);c[0]=vm.envString("LAB_PYTHON");c[1]=vm.envString("LAB_BRIDGE");for(uint i;i<a.length;i++)c[i+2]=a[i];return vm.ffi(c);}
 function setUp() public {vm.chainId(8453);vm.warp(1000);t=new MToken();string[] memory a=new string[](1);a[0]="pubkey";bytes32 key=bytes32(py(a));e=new VerdictGatedEscrow(IERC20(address(t)),key);other=new VerdictGatedEscrow(IERC20(address(t)),key);t.mint(payer,10e6);}
 function trial(string memory mode) internal returns(bool ok,uint256 delta){
  bool alien=keccak256(bytes(mode))==keccak256("signer");bool addr=keccak256(bytes(mode))==keccak256("address");bool chain=keccak256(bytes(mode))==keccak256("chain");bool replay=keccak256(bytes(mode))==keccak256("replay");
  VerdictGatedEscrow target=addr?other:e;uint256 id=target.escrowId(payer,salt);string[] memory a=new string[](7);a[0]="vector";a[1]=alien?"J_unauthorized":"positive";a[2]=vm.toString(address(e));a[3]=vm.toString(address(t));a[4]=vm.toString(id);a[5]=vm.toString(address(other));a[6]=vm.toString(id);Wire memory w=abi.decode(py(a),(Wire));
  vm.prank(payer);target.fund(salt,payee,1e6,w.request,w.policy,1,2000);bytes memory sig=abi.encodePacked(w.r,w.s);
  if(chain)vm.chainId(8454);if(replay){target.release(id,w.nonce,w.decision,sig);t.mint(address(target),1e6);}
  uint256 beforeBalance=t.balanceOf(payee);(ok,)=address(target).call(abi.encodeCall(target.release,(id,w.nonce,w.decision,sig)));delta=t.balanceOf(payee)-beforeBalance;
 }
 function test_distinguishing_witness_and_positive() public {
  uint256 snap=vm.snapshotState();(bool pos,uint256 pd)=trial("positive");assertTrue(pos);assertEq(pd,1e6);assertTrue(vm.revertToState(snap));
  (bool neg,uint256 nd)=trial(vm.envString("LAB_MUTATION_WITNESS"));string memory obj="boundary";vm.serializeBool(obj,"positive",pos);vm.serializeUint(obj,"positive_delta",pd);vm.serializeBool(obj,"negative_authorized",neg);vm.serializeUint(obj,"negative_delta",nd);string memory data=vm.serializeAddress(obj,"primary_address",address(e));vm.writeJson(data,string.concat(vm.envString("LAB_EVIDENCE_DIR"),"/boundary.json"));
 }
}
