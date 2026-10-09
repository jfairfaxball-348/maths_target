#!/usr/bin/env python3
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def txt(p): return (ROOT/p).read_text(encoding="utf8")
def main():
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
    assert state["session_completed"]=="S000" and state["active_paper_id"] is None and not state["child_repo_created"]
    projects=json.loads(txt("programme/PROJECTS.json")); assert projects["projects"]==[]
    assert "NOT VERBATIM" in txt("prompts/S000_INPUT.md")
    print("PASS: 10 candidates, 45 matches, scores, full bracket, ladders, parent/child state and handoffs")
if __name__=="__main__":main()
