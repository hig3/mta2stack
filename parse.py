#!/opt/local/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import re
import math

from lxml import etree
from copy import deepcopy

questiongroup={}
question={}

questionindex=set([])
groupindex=set([])


while True:
    line=""
    noline=False
    while True:
        a=sys.stdin.readline().rstrip()

        if not a:
            noline=True
            break
            
        line=line+a
        if line[-1:] is "@":
            line=line[:-1]
            break

    if noline:
        break

        
    try:
        words=line.split('.',3)


        if re.match("\d",words[2]):
            (key,value)=words[3].split("=",1)
            question[(int(words[1]),int(words[2]),key)]=value
            questionindex.add(int(words[2]))
        else:
            (key,value)=words[2].split("=",1)
            questiongroup[(int(words[1]),key)]=value
            groupindex.add(int(words[1]))
    except:
        raise

print questiongroup
print question
#print groupindex
#print questionindex

#for i in groupindex:
#    print questiongroup[ ( i,'topic')]
#    for j in questionindex:
#        print question[( i,j,'name')]
print "parsing finished"

questionxml=u"""
  <question type="stack">
    <name>
      <text>有理関数の微分1</text>
    </name>
    <questiontext format="html">
      <text><![CDATA[<p>次の関数を微分せよ.</p>
<p>\[ @ primitive @ \]</p>
<p>[[input:ans1]]</p>
<div>[[validation:ans1]]</div>]]></text>
    </questiontext>
    <generalfeedback format="html">
      <text></text>
    </generalfeedback>
    <defaultgrade>1.0000000</defaultgrade>
    <penalty>0.1000000</penalty>
    <hidden>0</hidden>
    <questionvariables>
      <text>a:rand(6)+2
n:rand(4)+2
b:rand(6)+1
m:rand(4)+2
primitive:(a*x^n+b)^m</text>
    </questionvariables>
    <specificfeedback format="html">
      <text><![CDATA[<p>[[feedback:prt1]]</p>]]></text>
    </specificfeedback>
    <questionnote>
      <text>1234</text>
    </questionnote>
    <questionsimplify>1</questionsimplify>
    <assumepositive>0</assumepositive>
    <prtcorrect format="html">
      <text><![CDATA[<p>正解です.</p>]]></text>
    </prtcorrect>
    <prtpartiallycorrect format="html">
      <text><![CDATA[<p>正しい部分もありますが, 正解ではありません.</p>]]></text>
    </prtpartiallycorrect>
    <prtincorrect format="html">
      <text><![CDATA[<p>正解ではありません.</p>]]></text>
    </prtincorrect>
    <multiplicationsign>dot</multiplicationsign>
    <sqrtsign>1</sqrtsign>
    <complexno>i</complexno>
    <inversetrig>cos-1</inversetrig>
    <matrixparens>[</matrixparens>
    <variantsselectionseed></variantsselectionseed>
    <input>
      <name>ans1</name>
      <type>algebraic</type>
      <tans>diff(primitive,x)</tans>
      <boxsize>15</boxsize>
      <strictsyntax>0</strictsyntax>
      <insertstars>1</insertstars>
      <syntaxhint></syntaxhint>
      <forbidwords>diff</forbidwords>
      <allowwords></allowwords>
      <forbidfloat>1</forbidfloat>
      <requirelowestterms>0</requirelowestterms>
      <checkanswertype>1</checkanswertype>
      <mustverify>1</mustverify>
      <showvalidation>1</showvalidation>
      <options></options>
    </input>
    <prt>
      <name>prt1</name>
      <value>1.0000000</value>
      <autosimplify>1</autosimplify>
      <feedbackvariables>
        <text></text>
      </feedbackvariables>
      <node>
        <name>0</name>
        <answertest>Diff</answertest>
        <sans>ans1</sans>
        <tans>diff(primitive,x)</tans>
        <testoptions>x</testoptions>
        <quiet>0</quiet>
        <truescoremode>=</truescoremode>
        <truescore>1.0000000</truescore>
        <truepenalty></truepenalty>
        <truenextnode>-1</truenextnode>
        <trueanswernote>prt1-1-T</trueanswernote>
        <truefeedback format="html">
          <text></text>
        </truefeedback>
        <falsescoremode>=</falsescoremode>
        <falsescore>0.0000000</falsescore>
        <falsepenalty></falsepenalty>
        <falsenextnode>-1</falsenextnode>
        <falseanswernote>prt1-1-F</falseanswernote>
        <falsefeedback format="html">
          <text></text>
        </falsefeedback>
      </node>
    </prt>
  </question>"""

qtree=etree.fromstring(questionxml)


root=etree.Element("quiz")

for i in groupindex:
    category = etree.SubElement(root,"question",type="category")
    categorytext=etree.SubElement(category,"text")
    categorytext.text=questiongroup[(i,'topic')]
#    root.append(etree.Element("question")).append(etree.Element("text")).text=questiongroup[(i,'topic')]

    for j in questionindex:
        q= deepcopy(qtree)
#        etree.SubElement(root,"question",type="stack")
#        name=etree.SubElement(q,"name")
        [ d for d in [ c for c in q if c.tag == "name" ][0] if d.tag=="text"][0].text=question[(i,j,'name')]
# if editing=uesHTML?
        [ d for d in [ c for c in q if c.tag == "questiontext" ][0] if d.tag=="text"][0].text=question[(i,j,'question')]
        [ d for d in [ c for c in q if c.tag == "input" ][0] if d.tag=="tans"][0].text=question[(i,j,'maple')]        # strip RESPONSE=
        [ e for e in [ d for d in [ c for c in q if c.tag == "prt" ][0] if d.tag=="node"][0] if e.tag=="tans"][0].text=question[(i,j,'maple')]
        [ f for f in [e for e in [ d for d in [ c for c in q if c.tag == "prt" ][0] if d.tag=="node"][0] if e.tag=="falsefeedback"][0] if f.tag=="text"][0].text=question[(i,j,'comment')]

        root.append(q)
                
print '<?xml version="1.0" encoding="UTF-8"?>'
print etree.tostring(root, encoding='utf-8', pretty_print=True)
