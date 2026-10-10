#!/usr/bin/env python3
import json
import re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def txt(p): return (ROOT/p).read_text(encoding="utf8")
def check_registration(state, projects, receipt):
    assert state["repo"] == projects["parent"] == receipt["parent"]["repository"] == "jfairfaxball-348/sunflower-structures-programme"
    assert state["repository_id"] == receipt["parent"]["repository_id"] == 1412469441
    assert state["session_completed"] == "S000" and state["next_programme_session"] == "S001"
    assert state["headline_id"] == "SUN" and state["champion"] == "Erdős–Rado Sunflower Conjecture"
    assert state["active_paper_id"] == projects["active_project"] == receipt["project_id"] == "P001"
    assert state["child_repo_created"] and state["first_paper_authorized"]
    assert not state["parent_repo_name_temporary"]
    assert len(projects["projects"]) == 1 and projects["planned"] == []
    project = projects["projects"][0]
    child = receipt["child"]
    assert project["repository_id"] == child["repository_id"] == 1412820282
    assert child["repository"] == "jfairfaxball-348/sunflower-internal-kernel-extraction"
    assert project["url"] == child["url"] == "https://github.com/" + child["repository"]
    sha = child["main_commit"]
    assert re.fullmatch(r"[0-9a-f]{40}", sha)
    assert project["verified_commit"] == sha == child["merged_pr"]["merge_sha"]
    assert child["merged_pr"]["merged"] and child["merged_pr"]["merged_at"]
    run = child["main_validation"]
    assert run["head_sha"] == sha and run["event"] == "push"
    assert run["status"] == "completed" and run["conclusion"] == "success"
    assert run["jobs"] and any(j["name"] == "validate" for j in run["jobs"])
    for job in run["jobs"]:
        assert job["id"] > 0 and job["status"] == "completed" and job["conclusion"] == "success"
        assert job["steps"] and all(s["conclusion"] == "success" for s in job["steps"])
    audit = receipt["independent_registration_verification"]
    for field in ("open_status", "novelty_status", "formal_status", "publication_status"):
        assert project[field] == audit[field]
    assert audit["open_status"] == "STRONG_EVIDENCE_OPEN"
    assert audit["novelty_status"] == "NOVELTY_UNCERTAIN"
    assert audit["formal_status"] == "NOT_STARTED" and audit["publication_status"] == "IDEA"
    assert state["mathematical_result_count"] == audit["new_theorems"] == 0
    assert state["formal_verifications"] == audit["formal_verifications"] == 0
    assert state["publications"] == audit["publications"] == 0
    next_step = receipt["next_child_obligation"]
    expected_successors = {"P001-S000": ("P001-S001", ["R3"]),
                           "P001-S001": ("P001-S002", ["L_AVG"]),
                           "P001-S002": ("P001-S003", ["L_AVG_HEAVY_LINK_CHARGING"]),
                           "P001-S003": ("P001-S004", ["L_AVG_COUNTEREXAMPLE_INDEPENDENT_AUDIT"]),
                           "P001-S004": ("P001-S005", ["FIVE_SESSION_PROGRESS_CORRECTION_AND_ROUTE_TRIAGE"]),
                           "P001-S005": ("P001-S006", ["HUMAN_PROGRAMME_DECISION_REQUIRED"])}
    expected_successors["P001-S006"] = ("P001-S007", ["HUMAN_BLOCK_COMPATIBILITY_DECISION_GATE"])
    expected_successors["P001-S007"] = ("P001-S008", ["HIGH_LOAD_VERTEX_RESERVOIR_COMPATIBILITY"])
    expected_successors["P001-S008"] = ("P001-S009", ["TWO_HUB_MULTIPLICITY_SLICE"])
    expected_successors["P001-S009"] = ("P001-S010", ["PRIVATE_LIGHT_MULTIHUB_COMPATIBILITY_AND_TENTH_AUDIT"])
    expected_successors["P001-S010"] = ("P001-S011", ["EXACT_PRIVATE_LIGHT_SINGLETON_LINK_MATCHING_CERTIFICATE"])
    if receipt.get("registration_kind") == "P001_S006_APPROVAL_ONLY":
        # Last substantive session remains S005; administrative approval changes its sole unexecuted successor.
        assert receipt["session"] == "P001-S005"
        expected_successors["P001-S005"] = ("P001-S006", ["BLOCK_COMPATIBILITY_FEASIBILITY_GATE"])
        approved = receipt["approved_next_child_handoff"]
        assert approved["session"] == "P001-S006" and approved["approved"] is True and approved["executed"] is False
        assert approved["child_main_commit"] == child["main_commit"]
        assert approved["method"] == "SUNFLOWER_BLOCK_COMPATIBILITY"
        assert approved["source_first_N1_performed"] is False and approved["mathematical_proof_performed"] is False
        assert audit["owner_decision_resolved_after_s005"] is True
        assert audit["new_mathematical_session_executed"] is False
        assert (ROOT / "sessions/P001-S006/APPROVAL_REGISTRATION.md").is_file()
    if receipt["session"] == "P001-S006":
        assert receipt["registration_kind"] == "P001_S006_SUBSTANTIVE_RESTRICTED_ONLY"
        assert receipt["independent_registration_verification"]["session_outcome"] == "RESTRICTED_BSEL_ONLY"
        assert receipt["independent_registration_verification"]["bsel_universal_proved"] is False
        assert receipt["independent_registration_verification"]["independent_mathematical_review"] is False
        assert (ROOT / "sessions/P001-S006/REGISTRATION.md").is_file()
    if receipt["session"] == "P001-S007":
        assert receipt["registration_kind"] == "P001_S007_PROOF_FIRST_RESTRICTED_LOW_LOAD"
        assert audit["session_outcome"] == "RESTRICTED_LOW_LOAD_BSEL_PROVED_NO_FULL_EXTRACTION"
        assert audit["bsel_universal_proved"] is False and audit["independent_mathematical_review"] is False
        assert audit["owner_policy"] == "PROOF_FIRST_TECHNICAL_METHOD_SELECTION_AUTONOMOUS_AND_PRIOR_ART_DEFERRED_UNTIL_COMPLETE_TIK_PROOF"
        assert project["last_child_session"] == "P001-S007"
        assert child["final_head_validation"] and all(x["head_sha"] == child["merged_pr"]["head_sha"] and x["conclusion"] == "success" for x in child["final_head_validation"])
        assert (ROOT / "sessions/P001-S007/REGISTRATION.md").is_file()
    if receipt["session"] == "P001-S008":
        assert receipt["registration_kind"] == "P001_S008_PROOF_FIRST_SINGLE_HUB_RESERVOIR_NEGATIVE"
        assert audit["session_outcome"] == "SINGLE_HUB_HIGH_LOAD_RESERVOIR_REFUTED_BSEL_OPEN"
        assert audit["single_hub_reservoir_refuted"] is True
        assert audit["single_hub_counterexample_full_union_valid"] is True
        assert audit["bsel_universal_proved"] is False and audit["bsel_universal_refuted"] is False
        assert audit["independent_mathematical_review"] is False
        assert audit["R3_TIK_refuted"] is False
        assert project["last_child_session"] == "P001-S008"
        assert child["final_head_validation"] and all(x["head_sha"] == child["merged_pr"]["head_sha"] and x["conclusion"] == "success" for x in child["final_head_validation"])
        assert (ROOT / "sessions/P001-S008/REGISTRATION.md").is_file()
    if receipt["session"] == "P001-S009":
        assert receipt["registration_kind"] == "P001_S009_TWO_HEAVY_THIN_Q_NEGATIVE_STATUS_ONLY"
        assert audit["session_outcome"] == "TWO_HEAVY_LOW_LOAD_THINNING_REFUTED_BSEL_OPEN"
        assert audit["two_heavy_thin_q_refuted"] is True
        assert audit["two_heavy_counterexample_full_union_valid"] is True
        assert audit["two_heavy_bsel_proved"] is False and audit["two_heavy_bsel_refuted"] is False
        assert audit["bsel_universal_proved"] is False and audit["bsel_universal_refuted"] is False
        assert audit["independent_mathematical_review"] is False and audit["R3_TIK_refuted"] is False
        assert project["last_child_session"] == "P001-S009"
        assert child["final_head_validation"] and all(x["head_sha"] == child["merged_pr"]["head_sha"] and x["conclusion"] == "success" for x in child["final_head_validation"])
        assert (ROOT / "sessions/P001-S009/REGISTRATION.md").is_file()
    if receipt["session"] == "P001-S010":
        assert receipt["registration_kind"] == "P001_S010_PRIVATE_LIGHT_SAT_CROSS_NEGATIVE_TENTH_AUDIT_STATUS_ONLY"
        assert audit["session_outcome"] == "PRIVATE_LIGHT_CROSS_HUB_CLOSURE_REFUTED_BSEL_OPEN_TENTH_AUDIT"
        assert audit["private_light_sat_cross_refuted"] and audit["private_light_control_valid_over_half"]
        assert audit["tenth_audit_completed"] and audit["s005_rechecked"]
        assert not audit["private_light_two_heavy_bsel_proved"] and not audit["private_light_two_heavy_bsel_refuted"]
        assert not audit["full_tik_proved"] and not audit["R3_TIK_refuted"]
        assert not audit["independent_mathematical_review"]
        assert project["last_child_session"] == "P001-S010"
        assert child["final_head_validation"] and all(x["head_sha"] == child["merged_pr"]["head_sha"] and x["conclusion"] == "success" for x in child["final_head_validation"])
        assert (ROOT / "sessions/P001-S010/REGISTRATION.md").is_file()
    expected_session, expected_objectives = expected_successors[receipt["session"]]
    assert next_step["session"] == expected_session and next_step["objectives"] == expected_objectives
    assert state["last_registry_update"] == receipt["session"]
    if receipt["session"] == "P001-S001":
        assert audit["session_outcome"] == "MECHANISM_OBSTRUCTION_AND_REMAINING_LEMMA"
        assert audit["r3_literature_status"] == "STATUS_UNCERTAIN"
        assert project["last_child_session"] == "P001-S001"
        assert child["final_head_validation"]
        for checked in child["final_head_validation"]:
            assert checked["head_sha"] == child["merged_pr"]["head_sha"]
            assert checked["conclusion"] == "success" and checked["jobs"]
            assert all(j["conclusion"] == "success" for j in checked["jobs"])
    if receipt["session"] == "P001-S002":
        assert audit["session_outcome"] == "RESTRICTED_SUNFLOWER_FREE_BOUND_GENERAL_L_AVG_UNRESOLVED"
        assert audit["r3_literature_status"] == "STATUS_UNCERTAIN"
        assert project["last_child_session"] == "P001-S002"
        assert len(child["final_head_validation"]) >= 1
        for checked in child["final_head_validation"][:1]:
            assert checked["head_sha"] == child["merged_pr"]["head_sha"]
            assert checked["conclusion"] == "success" and checked["jobs"]
            assert all(j["conclusion"] == "success" for j in checked["jobs"])
    if receipt["session"] == "P001-S003":
        assert audit["session_outcome"] == "NO_GENERAL_PROGRESS_L_AVG_REFUTED"
        assert audit["r3_literature_status"] == "STATUS_UNCERTAIN"
        assert audit["auxiliary_L_AVG_status"] == "COUNTEREXAMPLE_ON_PAPER_INDEPENDENT_REVIEW_PENDING"
        assert not audit["R3_TIK_refuted"]
        assert project["last_child_session"] == "P001-S003"
        assert child["final_head_validation"]
        for checked in child["final_head_validation"]:
            assert checked["head_sha"] == child["merged_pr"]["head_sha"]
            assert checked["conclusion"] == "success" and checked["jobs"]
            assert all(j["conclusion"] == "success" for j in checked["jobs"])
    if receipt["session"] == "P001-S004":
        assert audit["session_outcome"] == "NO_GENERAL_R3_PROGRESS_L_AVG_B_CHARGE_RETIRED"
        assert audit["r3_literature_status"] == "STATUS_UNCERTAIN"
        assert audit["auxiliary_L_AVG_status"] == "PROVISIONAL_ANALYTICALLY_SUPPORTED_COUNTEREXAMPLE_ROUTE_RETIRED"
        assert audit["heavy_link_B_CHARGE"] == "PROVISIONAL_ANALYTICALLY_SUPPORTED_COUNTEREXAMPLE_ROUTE_RETIRED"
        assert audit["independent_mathematical_review"] is False
        assert audit["R3_TIK_refuted"] is False
        assert project["last_child_session"] == "P001-S004"
        assert child["final_head_validation"]
        for checked in child["final_head_validation"]:
            assert checked["head_sha"] == child["merged_pr"]["head_sha"]
            assert checked["conclusion"] == "success" and checked["jobs"]
            assert all(j["conclusion"] == "success" for j in checked["jobs"])
    if receipt["session"] == "P001-S005":
        assert audit["session_outcome"] == "FIVE_SESSION_AUDIT_NO_APPROVED_SURVIVING_R3_ROUTE"
        assert audit["r3_literature_status"] == "STATUS_UNCERTAIN"
        assert audit["human_decision_required"] is True
        assert audit["new_mathematical_candidate_promoted"] is False
        assert audit["independent_mathematical_review"] is False
        assert audit["R3_TIK_refuted"] is False
        assert project["last_child_session"] == "P001-S005"
        assert child["final_head_validation"]
        for checked in child["final_head_validation"]:
            assert checked["head_sha"] == child["merged_pr"]["head_sha"]
            assert checked["conclusion"] == "success" and checked["jobs"]
            assert all(j["conclusion"] == "success" for j in checked["jobs"])
    if receipt["session"] == "P001-S006":
        assert project["last_child_session"] == "P001-S006"
        assert audit["r3_literature_status"] == "STATUS_UNCERTAIN" and not audit["R3_TIK_refuted"]
        assert child["final_head_validation"] and all(x["head_sha"] == child["merged_pr"]["head_sha"] and x["conclusion"] == "success" for x in child["final_head_validation"])
    assert next_step["open_status"] == "STATUS_UNCERTAIN"
    assert not next_step["executed"] and not project["next_executed"]
    assert not receipt["parent_programme_session_executed"]
    for observed in receipt["parent_registration_ci"]:
        assert re.fullmatch(r"[0-9a-f]{40}", observed["head_sha"])
        assert observed["conclusion"] == "success" and observed["jobs"]
        assert all(j["conclusion"] == "success" for j in observed["jobs"])
def main():
    for path in ROOT.rglob("*.json"):
        json.loads(path.read_text(encoding="utf8"))
    candidates=json.loads(txt("tournament/S000/data.json"))
    assert len(candidates)==10 and len({x["id"] for x in candidates})==10
    assert sum(candidates[0]["weights"])==100
    weights=candidates[0]["weights"]
    for c in candidates:
        assert len(c["scores"])==len(weights)==8
        assert all(0<=s<=w for s,w in zip(c["scores"],weights))
        assert c["score"]==sum(c["scores"]) 
        assert len(c["ladder"])==5
    matches=json.loads(txt("tournament/S000/matches.json"))
    assert len(matches)==45
    ids={x["id"] for x in candidates}
    pairs=set(); wins={x:0 for x in ids}; losses={x:0 for x in ids}
    for m in matches:
        a,b,w=m["a"],m["b"],m["winner"]
        assert a!=b and {a,b}<=ids and w in (a,b)
        pair=frozenset((a,b)); assert pair not in pairs; pairs.add(pair)
        wins[w]+=1;losses[b if w==a else a]+=1
    assert sum(wins.values())==sum(losses.values())==45
    assert all(wins[x]+losses[x]==9 for x in ids)
    bracket=json.loads(txt("tournament/S000/bracket.json"))
    ordered=sorted(candidates,key=lambda c:(-wins[c["id"]],-c["score"],c["id"]))
    assert bracket["seeds"]==[x["id"] for x in ordered[:4]]
    for m in bracket["semifinals"]+[bracket["championship"],bracket["third_place"]]:
        assert m["winner"] in (m["a"],m["b"])
        assert any({r["a"],r["b"]}=={m["a"],m["b"]} and r["winner"]==m["winner"] for r in matches)
    s1,s2=bracket["semifinals"]
    assert {bracket["championship"]["a"],bracket["championship"]["b"]}=={s1["winner"],s2["winner"]}
    assert bracket["championship"]["winner"]=="SUN"
    assert len(bracket["ranking"])==10 and set(bracket["ranking"])==ids
    required=["AGENTS.md","authoritative/STATE.json","authoritative/NOVELTY_STANDARD.md","authoritative/FORMALISATION_POLICY.md","programme/PROJECTS.json","papers/PAPER_01_BRIEF.md","papers/P001_S000_KICKOFF_PROMPT.md","sessions/NEXT_SESSION.md","sessions/S000/CLOSEOUT.md"]
    for p in required: assert (ROOT/p).is_file(),p
    state=json.loads(txt("authoritative/STATE.json"))
    projects=json.loads(txt("programme/PROJECTS.json"))
    receipt=json.loads(txt("programme/P001_REGISTRATION.json"))
    check_registration(state, projects, receipt)
    assert (ROOT/"sessions/P001-S000/REGISTRATION.md").is_file()
    assert (ROOT/"prompts/S001_BEFORE_P001_REGISTRATION.md").is_file()
    assert not (ROOT/"sessions/S001").exists(), "Registration is not parent S001"
    if receipt["session"] == "P001-S001":
        assert (ROOT/"sessions/P001-S001/REGISTRATION.md").is_file()
        assert (ROOT/"sessions/P001-S000/REGISTRATION_RECEIPT.json").is_file()
        assert (ROOT/"prompts/S001_BEFORE_P001_S001_STATUS.md").is_file()
    if receipt["session"] == "P001-S002":
        assert (ROOT/"sessions/P001-S002/REGISTRATION.md").is_file()
        assert (ROOT/"sessions/P001-S001/REGISTRATION_RECEIPT.json").is_file()
        assert (ROOT/"prompts/S001_BEFORE_P001_S002_STATUS.md").is_file()
    if receipt["session"] == "P001-S003":
        assert (ROOT/"sessions/P001-S003/REGISTRATION.md").is_file()
        assert (ROOT/"sessions/P001-S002/REGISTRATION.md").is_file()
    assert "NOT VERBATIM" in txt("prompts/S000_INPUT.md")
    print("PASS: 10 candidates, 45 matches, scores, full bracket, ladders, JSON, checked child registration, zero-result counts and separate handoffs")
if __name__=="__main__":main()

