#!/opt/local/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import re
import math
import string

from lxml import etree
from copy import deepcopy

questiongroup={}
question={}
questinhints={}

questionindex=set([])
groupindex=set([])

DEBUG=True
DEBUG=False
DOLLAR_PREFIX="SSSS"
displaysolution=False

while True:
    line=""
    noline=False
    while True:
        a=sys.stdin.readline()

        if not a:
            noline=True
            break
        
        line=line+a.rstrip()
        if line[-1:] is "@":
            line=line[:-1]
            break
        
    if noline:
        break

#   delete empty lines
#   if re.match(r'^\s*$',line):
#        print "afo"
#        continue

    try:
        words=line.split('.',3)

        #extract word[3]="hint.1=text"
#        if re.match("\d",words[2]) and re.match("\d",word[4]) and word[3]=="hint":
#            (k,value)=words[4].split("=",1)
#            questionhints[(int(words[1]),int(words[2]),word[3],k)]=value
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

    if DEBUG:
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
        <answertest>AlgEquiv</answertest>
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
    firstquestion = etree.SubElement(root,"question",type="category")
    category = etree.SubElement(firstquestion,"category")
    categorytext=etree.SubElement(category,"text")
    categorytext.text=questiongroup[(i,'topic')]

    for j in questionindex:
        q= deepcopy(qtree)
        try:
            [ d for d in [ c for c in q if c.tag == "name" ][0] if d.tag=="text"][0].text=question[(i,j,'name')].decode('utf-8')
# if editing=uesHTML?
            [ d for d in [ c for c in q if c.tag == "questiontext" ][0] if d.tag=="text"][0].text=etree.CDATA(re.sub(r'\$(\w+)',r'@SSSS\1@',question[(i,j,'question')]).decode('utf-8')+ "<p>[[input:ans1]]</p><div>[[validation:ans1]]</div>")

            # Shown to everyone in the study session
            #            [ f for f in [e for e in [ d for d in [ c for c in q if c.tag == "prt" ][0] if d.tag=="node"][0] if e.tag=="falsefeedback"][0] if f.tag=="text"][0].text=etree.CDATA(re.sub(r'\$(\w+)',r'@SSSS\1@',question[(i,j,'solution')]))

            #            [ d for d in [ c for c in q if c.tag == "generalfeedback" ][0] if d.tag=="text"][0].text=etree.CDATA(re.sub(r'\$(\w+)',r'SSSS\1',question[(i,j,'solution')]))
            tempstr=question[(i,j,'algorithm')].replace('$',DOLLAR_PREFIX)
            deststr=tempstr.translate(string.maketrans('=;',':\n'),'$')
            deststr=re.sub(r'maple\("printf\(\s*MathML\[ExportPresentation\]\((.+?)\)\)"\)',r'\1', deststr)
            deststr=re.sub(r'maple\("(.+?)"\)',r'\1', deststr)
            deststr=re.sub(r'range\(\s*(-?\d)\s*,\s*(-?\d)\s*,\s*(-?\d)\s*\)',r'rand_with_step(\1,\2,\3)', deststr)
            deststr=re.sub(r'range\(\s*(-?\d),\s*(-?\d)\)',r'rand_with_step(\1,\2,1)', deststr)            

          
            [ d for d in [ c for c in q if c.tag == "questionvariables" ][0] if d.tag=="text"][0].text='/*'+tempstr+'*/'+'\n'+'/*'+deststr+'*/'

            [ d for d in [ c for c in q if c.tag == "questionnote" ][0] if d.tag=="text"][0].text=re.sub(r'\$(\w+)',r'@SSSS\1@',re.sub(r'=.*?;',r',',question[(i,j,'algorithm')]))

            if (i,j,'maple_answer') in question:
                answer=question[(i,j,'maple_answer')].replace('$',DOLLAR_PREFIX)
            elif (i,j,'answer.num') in question:
                answer=question[(i,j,'answer.num')].replace('$',DOLLAR_PREFIX)
            else:
                answer=DOLLAR_PREFIX + 'ans';

# TODO: ans1, validation
            [ d for d in [ c for c in q if c.tag == "input" ][0] if d.tag=="tans"][0].text=answer
                
            [ e for e in [ d for d in [ c for c in q if c.tag == "prt" ][0] if d.tag=="node"][0] if e.tag=="tans"][0].text=answer

#  titled feedback in Maple T.A., shown to everyone                
            [ d for d in [ c for c in q if c.tag == "generalfeedback" ][0] if d.tag=="text"][0].text=etree.CDATA(re.sub(r'\$(\w+)',r'@SSSS\1@',question[(i,j,'comment')]).decode('utf-8'))
            
            [ d for d in [ c for c in q if c.tag == "prtcorrect" ][0] if d.tag=="text"][0].text=etree.CDATA(u"<p>正解です.</p>")
            [ d for d in [ c for c in q if c.tag == "prtpartiallycorrect" ][0] if d.tag=="text"][0].text=etree.CDATA(u"<p>正しい部分もありますが, 正解ではありません.</p>")
            [ d for d in [ c for c in q if c.tag == "prtincorrect" ][0] if d.tag=="text"][0].text=etree.CDATA(u"<p>正解ではありません.</p>")

            for k in question:
                if k[0]==i and k[1]==j and re.match('^hint.\d$',k[2]):
                    tmp=etree.Element("text")
                    tmp.text=etree.CDATA(re.sub(r'\$(\w+)',r'@SSSS\1@',question[k]))
                    tmp2=etree.Element("hint")
                    tmp2.append(tmp)
                    q.append(tmp2)

# truefeedback            

        except IndexError:
            print i,j
            raise


        
        root.append(q)
                
print '<?xml version="1.0" encoding="UTF-8"?>'
print etree.tostring(root, encoding='utf-8', pretty_print=True)

# description not touched
# solution is for study session

# qu.1.1.uid=0b96da37-a4b5-4d16-a445-3fd0e346d164@
# qu.1.1.privacy=10@
# qu.1.1.allowRepublish=false@
# qu.1.1.description=@
# qu.1.1.difficulty=0.0@
# qu.1.1.modifiedIn=10@
# qu.1.1.modifiedBy=004d8747-b5c4-411e-830b-864b7c1cfde1@
# qu.1.1.school=97620e6e-18ef-4cee-b3ac-349dd2f621ae@
# qu.1.1.attributeAuthor=true@
# qu.1.1.numberOfAttempts=1@
# qu.1.1.numberOfAttemptsLeft=1@
# qu.1.1.numberOfTryAnother=0@
# qu.1.1.numberOfTryAnotherLeft=0@
# qu.1.1.description=description@

# qu.1.1.hint.1=<p>hint1test</p>@
# qu.1.1.hint.1.name=hint1@
# qu.1.1.hint.1.description=@
# qu.1.1.hint.1.penalty=0.0@
# qu.1.1.hint.1.modified=1433825957879@
# qu.1.1.hint.2=<p>hint2text</p>@

