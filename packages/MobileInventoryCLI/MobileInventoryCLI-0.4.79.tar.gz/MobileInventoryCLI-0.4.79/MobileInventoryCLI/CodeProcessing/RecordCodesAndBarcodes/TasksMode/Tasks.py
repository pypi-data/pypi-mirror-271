from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.DB.db import *
import MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.Unified.Unified as unified
import MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.possibleCode as pc
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.DB.Prompt import *
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.DB.Prompt import prefix_text
import random
from pint import UnitRegistry
import pandas as pd
import numpy as np
from datetime import *
from colored import Style,Fore
import json,sys

class TasksMode:
    #extra is for future expansion
    def exportList2Excel(self,fields=False,extra=[]):
        FIELDS=['Barcode','ALT_Barcode','Code','Name','Price','CaseCount']
        cols=[i.name for i in Entry.__table__.columns]
        if fields == True:
            return FIELDS
        for i in extra:
            if i in cols:
                FIELDS.append(extra)
            else:
                print(f"{Fore.light_red}{Style.bold}Warning {Style.underline}{Style.reset}{Fore.light_yellow}'{i}' from extra={extra} is not a valid {Style.reset}{Fore.light_green}Field|Column!{Style.reset}")
       
        with Session(self.engine) as session:
            query=session.query(Entry).filter(Entry.InList==True)
            df = pd.read_sql(query.statement, query.session.bind)
            df=df[['Barcode','ALT_Barcode','Code','Name','Price','CaseCount']]
            #df.to_excel()
            def mkT(text,self):
                if text=='':
                    return 'InList-Export.xlsx'
                return text
            while True:
                try:
                    efilename=Prompt.__init2__(None,func=mkT,ptext=f"Save where[{mkT('',None)}]",helpText="save the data to where?",data=self)
                    if isinstance(efilename,str):
                        df.to_excel(efilename)
                    break
                except Exception as e:
                    print(e)
    def getTotalwithBreakDownForScan(self,short=False):
        while True:
            color1=Fore.red
            color2=Fore.yellow
            color3=Fore.cyan
            color4=Fore.green_yellow
            def mkT(text,self):
                return text
            scanned=Prompt.__init2__(None,func=mkT,ptext='barcode|code[help]?',helpText='',data=self)
            if not scanned:
                break
            else:
                with Session(self.engine) as session:
                    result=session.query(Entry).filter(or_(Entry.Barcode==scanned,Entry.Code==scanned,Entry.ALT_Barcode==scanned),Entry.InList==True).first()
                    if result:
                        backroom=result.BackRoom
                        total=0
                        for f in self.valid_fields:
                            if f not in self.special:
                                if getattr(result,f) not in [None,'']:
                                    total+=float(getattr(result,f))
                        if not short:
                            print(result)
                        else:
                            print(result.seeShort())
                        print(f"{Fore.light_yellow}0 -> {color1}Amount Needed Total+BackRoom {Style.reset}{color2}{Style.bold}{total}{Style.reset}! {Fore.grey_70}#if you total everything including backroom{Style.reset}")
                        print(f"{Fore.cyan}1 -> {color1}Amount Needed Total w/o BackRoom {Style.reset}{color2}{Style.bold}{total-backroom}{Style.reset} {Fore.grey_70}#if you are totalling everything without the backroom!{Style.reset}")
                        print(f"{Fore.light_green}2 -> {color1}Amount Needed Total w/o BackRoom - BackRoom {Style.reset}{color2}{Style.bold}{(total-backroom)-backroom}{Style.reset}! {Fore.grey_70}#if you are totalling everything needed minus what was/will brought from the backroom{Style.reset}")


                        
                    else:
                        print(f"{Fore.red}{Style.bold}No such Barcode|Code with InList==True:{scanned}{Style.reset}\nLet's Try a Search[*]!")
                        #search_auto_insert
                        idF=self.SearchAuto(InList=True,skipReturn=False)
                        if idF:
                            result=session.query(Entry).filter(Entry.EntryId==idF).first()
                            if result:
                                backroom=result.BackRoom
                                total=0
                                for f in self.valid_fields:
                                    if f not in self.special:
                                        if getattr(result,f) not in [None,'']:
                                            total+=float(getattr(result,f))
                                if not short:
                                    print(result)
                                else:
                                    print(result.seeShort())
                                print(f"{Fore.light_yellow}0 -> {color1}Amount Needed Total+BackRoom {Style.reset}{color2}{Style.bold}{total}{Style.reset}! {Fore.grey_70}#if you total everything including backroom{Style.reset}")
                                print(f"{Fore.cyan}1 -> {color1}Amount Needed Total w/o BackRoom {Style.reset}{color2}{Style.bold}{total-backroom}{Style.reset} {Fore.grey_70}#if you are totalling everything without the backroom!{Style.reset}")
                                print(f"{Fore.light_green}2 -> {color1}Amount Needed Total w/o BackRoom - BackRoom {Style.reset}{color2}{Style.bold}{(total-backroom)-backroom}{Style.reset}! {Fore.grey_70}#if you are totalling everything needed minus what 'was', or 'will be', brought from the backroom{Style.reset}")
                            else:
                                print(f"{Fore.light_yellow}Nothing was selected!{Style.reset}")




            

    def display_field(self,fieldname,load=False,above=None,below=None):
        color1=Fore.red
        color2=Fore.yellow
        color3=Fore.cyan
        color4=Fore.green_yellow
        m=f"Item Num |Name|Barcode|ALT_Barcode|Code|{fieldname}|EID"
        hr='-'*len(m)
        print(f"{m}\n{hr}")
        if (fieldname in self.valid_fields) or (load == True and fieldname == 'ListQty'):
            with Session(self.engine) as session:
                query=session.query(Entry).filter(Entry.InList==True)
                if above == None:
                    def mkT(text,self):
                        try:
                            v=int(text)
                        except Exception as e:
                            print(e)
                            v=0
                        return v
                    above=Prompt.__init2__(None,func=mkT,ptext=f"Above [{Fore.light_green}0{Style.reset}]",helpText="anything below this will not be displayed!",data=self)
                if below == None:
                    def mkTBelow(text,self):
                        try:
                            v=int(text)
                        except Exception as e:
                            print(e)
                            v=sys.maxsize
                        return v
                    below=Prompt.__init2__(None,func=mkTBelow,ptext=f"Below [{Fore.light_green}{sys.maxsize}{Style.reset}]",helpText="anything above this will not be displayed!",data=self)
                if above != None:
                    print(type(above),above,fieldname)
                    query=query.filter(getattr(Entry,fieldname)>above)
                if below != None:
                    query=query.filter(getattr(Entry,fieldname)<below)
                results=query.all()
                if len(results) < 1:
                    print(f"{Fore.red}{Style.bold}Nothing is in List!{Style.reset}")
                for num,result in enumerate(results):
                    print(f"{Fore.red}{num}{Style.reset} -> {color1}{result.Name}{Style.reset}|{color2}{result.Barcode}|{result.ALT_Barcode}{Style.reset}|{color3}{result.Code}{Style.reset}|{color4}{getattr(result,fieldname)}{Style.reset}|{Fore.yellow}{getattr(result,'EntryId')}{Style.reset}")
        print(f"{m}\n{hr}")

    def SearchAuto(self,InList=None,skipReturn=False):
        while True:
            try:
                with Session(self.engine) as session:
                    def mkT(text,self):
                        return text
                    fields=[i.name for i in Entry.__table__.columns if str(i.type) == "VARCHAR"]
                    stext=Prompt.__init2__(None,func=mkT,ptext="Search[*]:",helpText="Search All(*) fields",data=self)
                    query=session.query(Entry)
                    if not stext:
                        break
                    
                    q=[]
                    for f in fields:
                        q.append(getattr(Entry,f).icontains(stext.lower()))

                    query=query.filter(or_(*q))
                    if InList != None:
                        query=query.filter(Entry.InList==InList)
                    results=query.all()
                    ct=len(results)
                    for num,r in enumerate(results):
                        if num < round(0.25*ct,0):
                            color_progress=Fore.green
                        elif num < round(0.50*ct,0):
                            color_progress=Fore.light_green
                        elif num < round(0.75*ct,0):
                            color_progress=Fore.light_yellow
                        else:
                            color_progress=Fore.light_red
                        if num == ct - 1:
                            color_progress=Fore.red
                        if num == 0:
                            color_progress=Fore.cyan    
                        msg=f"{color_progress}{num}{Style.reset}/{Fore.light_red}{ct-1}{Style.reset} ->{r}"
                        print(msg)
                    print(f"{Fore.light_yellow}There are {Fore.light_red}{ct}{Fore.light_yellow} Total Results for search {Fore.medium_violet_red}'{stext}'{Style.reset}{Fore.light_yellow}.{Style.reset}")
                    print(f"{Fore.light_red}Fields Searched in {Fore.cyan}{fields}{Style.reset}")
                    def mklint(text,data):
                        try:    
                            if text.lower() in ['r','rs','rst','reset']:
                                return True
                            index=int(text)
                            if index in [i for i in range(data)]:
                                return index
                            else:
                                raise Exception("out of bounds!")
                        except Exception as e:
                            print(e)
                            return None
                    if skipReturn:
                        return
                    ct=len(results)-1
                    if ct+1 > 0:
                        reset=False
                        while True:
                            which=Prompt.__init2__(None,func=mklint,ptext=f"Which {Fore.light_red}entry # {Style.reset}{Fore.light_yellow}do you wish to use?",helpText="number of entry to use [0..{ct}]\nUse 'r'|'rs'|'rst'|'reset' to reset search\n",data=ct+1)
                            if which in [None,]:
                                return
                            elif which in [True,]:
                                reset=True
                                break
                            return results[which].EntryId
                        if reset == False:
                            break
            except Exception as e:
                print(e)


    def setFieldInList(self,fieldname,load=False):
        tmp_fieldname=fieldname
        while True:
            if (fieldname not in self.special or fieldname in ['Facings'] )or (load==True and fieldname in ['ListQty',]):
                m=f"Item Num |Name|Barcode|ALT_Barcode|Code|{fieldname}|EID"
                hr='-'*len(m)
                if (fieldname in self.valid_fields) or (load==True and fieldname in ['ListQty',]) or fieldname == None:
                    with Session(self.engine) as session:
                        code=''
                        
                        def mkT(text,self):
                            return str(text)
                        code=Prompt.__init2__(None,func=mkT,ptext="barcode|code",helpText=self.helpText_barcodes,data=self)
                        if code == None:
                            break
                        pc.PossibleCodes(scanned=code)
                        pc.PossibleCodesEAN13(scanned=code)
                            
                        value=0
                        def mkT(text,self):
                            try:
                                tmp=text.split(',')
                                if len(tmp) == 2:
                                    text,suffix=tmp
                                    if suffix.lower() not in ['s','e','u',' ','','c']:
                                        suffix=''
                                else:
                                    suffix=''
                                    for i in ['s','e','u','c']:
                                        if text.endswith(i):
                                            suffix=i
                                            text=text[:-1]
                                            break

                                return float(eval(text)),text,suffix
                            except Exception as e:
                                print(e)
                                return float(0),text,''
                        if fieldname == None:
                            hstring=f'''
Location Fields:
{Fore.deep_pink_3b}Shelf{Style.reset}
{Fore.light_steel_blue}BackRoom{Style.reset}
{Fore.cyan}Display_1{Style.reset}
{Fore.cyan}Display_2{Style.reset}
{Fore.cyan}Display_3{Style.reset}
{Fore.cyan}Display_4{Style.reset}
{Fore.cyan}Display_5{Style.reset}
{Fore.cyan}Display_6{Style.reset}
{Fore.cyan}SBX_WTR_DSPLY{Style.reset}
{Fore.cyan}SBX_CHP_DSPLY{Style.reset}
{Fore.cyan}SBX_WTR_KLR{Style.reset}
{Fore.violet}FLRL_CHP_DSPLY{Style.reset}
{Fore.violet}FLRL_WTR_DSPLY{Style.reset}
{Fore.grey_50}WD_DSPLY{Style.reset}
{Fore.grey_50}CHKSTND_SPLY{Style.reset}'''
                            def mkfields(text,data):
                                try:
                                    fields=tuple([i.name for i in Entry.__table__.columns])
                                    fields_lower=tuple([i.lower() for i in fields])
                                    if text.lower() in fields_lower:
                                        index=fields_lower.index(text.lower())
                                        return fields[index]
                                except Exception as e:
                                    print(e)
                            while True:
                                fieldname=Prompt.__init2__(None,func=mkfields,ptext="Location Field(see h|help)",helpText=hstring,data=self)
                                if fieldname in [None,]:
                                    break
                                break
                            if fieldname in [None,]:
                                continue
                            m=f"Item Num |Name|Barcode|ALT_Barcode|Code|{fieldname}|EID"
                            hr='-'*len(m)

                        p=Prompt.__init2__(None,func=mkT,ptext="amount|+amount|-amount",helpText=self.helpText_barcodes,data=self)
                        if p:
                            value,text,suffix=p
                        else:
                            continue
                        try:
                            color1=Fore.red
                            color2=Fore.yellow
                            color3=Fore.cyan
                            color4=Fore.green_yellow 
                            if text.startswith("-") or text.startswith("+"):
                                result=session.query(Entry).filter(or_(Entry.Barcode==code,Entry.Code==code,ENtry.ALT_Barcode==code)).first()
                                if result:
                                    if suffix.lower() in ['c',]:
                                        if result.CaseCount in [None,]:
                                            result.CaseCount=1
                                            session.commit()
                                            session.flush()
                                            session.refresh(result)
                                        if result.CaseCount < 1:
                                            result.CaseCount=1
                                            session.commit()
                                            session.flush()
                                            session.refresh(result)
                                        value=float(value)*result.CaseCount
                                    setattr(result,fieldname,getattr(result,fieldname)+float(value))
                                    result.InList=True
                                    session.commit()
                                    session.flush()
                                    session.refresh(result)
                                    print(f"{Fore.red}0{Style.reset} -> {color1}{result.Name}{Style.reset}|{color2}{result.Barcode}|{result.ALT_Barcode}{Style.reset}|{color3}{result.Code}{Style.reset}|{color4}{getattr(result,fieldname)}{Style.reset}|{color4}{getattr(result,'EntryId')}{Style.reset}")
                                    print(f"{m}\n{hr}")
                                else:
                                    replacement=self.SearchAuto()
                                    if isinstance(replacement,int):
                                        result=session.query(Entry).filter(Entry.EntryId==replacement).first()
                                        if result:
                                            setattr(result,fieldname,getattr(result,fieldname)+float(value))
                                            result.InList=True
                                            session.commit()
                                            session.flush()
                                            session.refresh(result)
                                            print(f"{Fore.red}0{Style.reset} -> {color1}{result.Name}{Style.reset}|{color2}{result.Barcode}|{result.ALT_Barcode}{Style.reset}|{color3}{result.Code}{Style.reset}|{color4}{getattr(result,fieldname)}{Style.reset}|{color4}{getattr(result,'EntryId')}{Style.reset}")
                                            print(f"{m}\n{hr}")
                                        else:
                                            raise Exception(f"result is {result}")
                                    else:
                                        name=code
                                        while True:
                                            try:
                                                def mkString(text,data):
                                                    return text
                                                name=Prompt.__init2__(None,func=mkString,ptext="Entry Name",helpText="Enter a name, or leave blank to use scanned code!",data=self)
                                                if name in [None,'']:
                                                    name=code
                                                break
                                            except Exception as e:
                                                print(e)
                                        icode=code
                                        while True:
                                            try:
                                                def mkString(text,data):
                                                    return text
                                                icode=Prompt.__init2__(None,func=mkString,ptext="Entry Code",helpText="Enter a Code, or leave blank to use scanned code as Code!",data=self)
                                                if icode in [None,'']:
                                                    icode=code
                                                break
                                            except Exception as e:
                                                print(e)
                                        iprice=0
                                        while True:
                                            try:
                                                def mkFloat(text,data):
                                                    try:
                                                        return float(eval(text))
                                                    except Exception as e:
                                                        return float(0)
                                                iprice=Prompt.__init2__(None,func=mkFloat,ptext="Entry Price",helpText="Enter a Price, or leave blank to use $0.00!",data=self)
                                                if iprice in [None,'']:
                                                    iprice=0
                                                break
                                            except Exception as e:
                                                print(e)
                                        icc=1
                                        while True:
                                            try:
                                                def mkint(text,data):
                                                    try:
                                                        return int(eval(text))
                                                    except Exception as e:
                                                        return int(1)
                                                icc=Prompt.__init2__(None,func=mkFloat,ptext="Entry Price",helpText="Enter a Price, or leave blank to use $0.00!",data=self)
                                                if icc in [None,'']:
                                                    icc=1
                                                break
                                            except Exception as e:
                                                print(e)
                                        n=Entry(Barcode=code,Code=icode,Price=iprice,Name=name,CaseCount=icc,InList=True,Note="New Item")
                                        setattr(n,fieldname,value)
                                        session.add(n)
                                        session.commit()
                                        session.flush()
                                        session.refresh(n)
                                        result=n
                                        print(f"{Fore.red}0{Style.reset} -> {color1}{result.Name}{Style.reset}|{color2}{result.Barcode}|{result.ALT_Barcode}{Style.reset}|{color3}{result.Code}{Style.reset}|{color4}{getattr(result,fieldname)}{Style.reset}|{color4}{getattr(result,'EntryId')}{Style.reset}")

                                        print(f"{m}\n{hr}")
                            else:
                                result=session.query(Entry).filter(or_(Entry.Barcode==code,Entry.Code==code,Entry.ALT_Barcode==code)).first()
                                if result:
                                    if suffix.lower() in ['c',]:
                                        if result.CaseCount in [None,]:
                                            result.CaseCount=1
                                            session.commit()
                                            session.flush()
                                            session.refresh(result)
                                        if result.CaseCount < 1:
                                            result.CaseCount=1
                                            session.commit()
                                            session.flush()
                                            session.refresh(result)
                                        value=float(value)*result.CaseCount
                                    setattr(result,fieldname,value)
                                    result.InList=True
                                    session.commit()
                                    session.flush()
                                    session.refresh(result)
                                    print(f"{Fore.red}0{Style.reset} -> {color1}{result.Name}{Style.reset}|{color2}{result.Barcode}|{result.ALT_Barcode}{Style.reset}|{color3}{result.Code}{Style.reset}|{color4}{getattr(result,fieldname)}{Style.reset}|{color4}{getattr(result,'EntryId')}{Style.reset}")

                                    print(f"{m}\n{hr}")

                                else:
                                    replacement=self.SearchAuto()
                                    if isinstance(replacement,int):
                                        result=session.query(Entry).filter(Entry.EntryId==replacement).first()
                                        if result:
                                            setattr(result,fieldname,getattr(result,fieldname)+float(value))
                                            result.InList=True
                                            session.commit()
                                            session.flush()
                                            session.refresh(result)
                                            print(f"{Fore.red}0{Style.reset} -> {color1}{result.Name}{Style.reset}|{color2}{result.Barcode}|{result.ALT_Barcode}{Style.reset}|{color3}{result.Code}{Style.reset}|{color4}{getattr(result,fieldname)}{Style.reset}|{color4}{getattr(result,'EntryId')}{Style.reset}")
                                            print(f"{m}\n{hr}")
                                        else:
                                            raise Exception(f"result is {result}")
                                    else:
                                        name=code
                                        while True:
                                            try:
                                                def mkString(text,data):
                                                    return text
                                                name=Prompt.__init2__(None,func=mkString,ptext="Entry Name",helpText="Enter a name, or leave blank to use scanned code!",data=self)
                                                if name in [None,'']:
                                                    name=code
                                                break
                                            except Exception as e:
                                                print(e)
                                        icode=code
                                        while True:
                                            try:
                                                def mkString(text,data):
                                                    return text
                                                icode=Prompt.__init2__(None,func=mkString,ptext="Entry Code",helpText="Enter a Code, or leave blank to use scanned code as Code!",data=self)
                                                if icode in [None,'']:
                                                    icode=code
                                                break
                                            except Exception as e:
                                                print(e)
                                        iprice=0
                                        while True:
                                            try:
                                                def mkFloat(text,data):
                                                    try:
                                                        return float(eval(text))
                                                    except Exception as e:
                                                        return float(0)
                                                iprice=Prompt.__init2__(None,func=mkFloat,ptext="Entry Price",helpText="Enter a Price, or leave blank to use $0.00!",data=self)
                                                if iprice in [None,'']:
                                                    iprice=0
                                                break
                                            except Exception as e:
                                                print(e)
                                        icc=1
                                        while True:
                                            try:
                                                def mkint(text,data):
                                                    try:
                                                        return int(eval(text))
                                                    except Exception as e:
                                                        return int(1)
                                                icc=Prompt.__init2__(None,func=mkFloat,ptext="Entry CaseCount",helpText="Enter a CaseCount, or leave blank to use 1!",data=self)
                                                if icc in [None,'']:
                                                    icc=1
                                                break
                                            except Exception as e:
                                                print(e)
                                        n=Entry(Barcode=code,Code=icode,Name=name,Price=iprice,CaseCount=icc,InList=True,Note="New Item")
                                        setattr(n,fieldname,value)
                                        session.add(n)
                                        session.commit()
                                        session.flush()
                                        session.refresh(n)
                                        result=n
                                        print(f"{Fore.red}0{Style.reset} -> {color1}{result.Name}{Style.reset}|{color2}{result.Barcode}|{result.ALT_Barcode}{Style.reset}|{color3}{result.Code}{Style.reset}|{color4}{getattr(result,fieldname)}{Style.reset}|{color4}{getattr(result,'EntryId')}{Style.reset}")

                                        print(f"{m}\n{hr}")

                                    #raise Exception(result)
                        except Exception as e:
                            print(e)
            else:
                #code for tags,caseId[br,6w,ld],
                self.processSpecial(fieldname)
                break
            if tmp_fieldname == None:
                fieldname=None
    helpText_barcodes=f"""
1. Enter the EntryId into the prompt
2. if an entry is found you will be prompted for a code to be saved
Quantity Modifiers:
(SEP=',' or No Sep) Suffixes Singles: s|e|u|' '|'' == units/singles/eaches/no multipliers
(SEP=',' or No Sep) Suffixes CaseCount: c == (qty*casecount+old_value_if_any
Valid Examples:
+1-2u - do operation in units and remove from qty 
-1+2c - do operation in cases and remove from qty
1c - cases set
1u - units set
remember, formula is calculated first, then that value is removed from qty if -/+
if CaseCount is less than 1, or not set, assume casecount == 1
    """
    def setBarcodes(self,fieldname):
         while True:
            try:
                def mkT(text,self):
                    return text
                cmd=Prompt.__init2__(None,func=mkT,ptext='Do What[help/q/b/$EntryId]?',helpText=self.helpText_barcodes,data=self)
                if not cmd:
                    break
                else:
                    with Session(self.engine) as session:
                        r=session.query(Entry).filter(Entry.EntryId==int(cmd)).first()
                        if r:
                            def mkT(text,self):
                                return text
                            code=Prompt.__init2__(None,func=mkT,ptext=f'{fieldname}[help]?',helpText=self.helpText_barcodes,data=self)
                            if not code:
                                break
                            else:
                                setattr(r,fieldname,code)
                                session.commit()
                                session.flush()
                                session.refresh(r)
                                print(r)
            except Exception as e:
                print(e)



    def processSpecial(self,fieldname):
        if fieldname.lower() == "tags":
            self.editTags()
        elif 'Barcode' in fieldname:
            self.setBarcodes(fieldname)
        else:
            print("SpecialOPS Fields! {fieldname} Not Implemented Yet!")
            self.editCaseIds()


    helpText_caseIds=f'''
{Fore.green_yellow}$WHERE,$EntryId,exec()|$ID{Style.reset}
#[ld,6w,br,all],$EntryId,generate - create a synthetic id for case and save item to and save qrcode png of $case_id in $WHERE
#[ld,6w,br,all],$EntryId,$case_id - set case id for item in $WHERE
#[ld,6w,br,all],$EntryId - display item case id in $WHERE
[ld,6w,br,all],s|search,$case_id - display items associated with $case_id in $WHERE
#[ld,6w,br,all],$EntryId,clr_csid - set $case_id to '' in $WHERE
where:
 ld is for Load
 6w is 6-Wheeler or U-Boat
 br is BackRoom
 
 all will apply to all of the above fields
    '''
    def editCaseIds(self):
         while True:
            def mkT(text,self):
                return text
            cmd=Prompt.__init2__(None,func=mkT,ptext='Do What[help]?',helpText=self.helpText_tags,data=self)
            if not cmd:
                break
            else:
                print(cmd)
                split_cmd=cmd.split(",")
                if len(split_cmd)==3:
                    mode=split_cmd[0]
                    eid=split_cmd[1]
                    ex=split_cmd[2]
                    if eid.lower() in ['s','search']:
                        #search
                        with Session(self.engine) as session:
                            results=[]
                            if split_cmd[0].lower() == '6w':
                                results=session.query(Entry).filter(Entry.CaseID_6W==ex).all()
                            elif split_cmd[0].lower() == 'ld':
                                results=session.query(Entry).filter(Entry.CaseID_LD==ex).all()
                            elif split_cmd[0].lower() == 'br':
                                results=session.query(Entry).filter(Entry.CaseID_BR==ex).all()
                            elif split_cmd[0].lower() == 'all':
                                results=session.query(Entry).filter(or_(Entry.CaseID_BR==ex,Entry.CaseID_LD==ex,Entry.CaseID_6W==ex)).all()
                            if len(results) < 1:
                                print(f"{Fore.dark_goldenrod}No Items to display!{Style.reset}")
                            for num,r in enumerate(results):
                                print(f"{Fore.red}{num}{Style.reset} -> {r}")
                    else:
                        with Session(self.engine) as session:
                            query=session.query(Entry).filter(Entry.EntryId==int(eid)).first()
                            if query:
                                if ex.lower() in ['clr_csid',]:
                                    if split_cmd[0].lower() == '6w':
                                        query.CaseID_6W=''
                                    elif split_cmd[0].lower() == 'ld':
                                        query.CaseID_LD=''
                                    elif split_cmd[0].lower() == 'br':
                                        query.CaseID_BR=''
                                    elif split_cmd[0].lower() == 'all':
                                        query.CaseID_6W=''
                                        query.CaseID_LD=''
                                        query.CaseID_BR=''
                                elif ex.lower() in ['generate','gen','g']:
                                    if split_cmd[0].lower() == '6w':
                                        query.CaseID_6W=query.synthetic_field_str()
                                    elif split_cmd[0].lower() == 'ld':
                                        query.CaseID_LD=query.synthetic_field_str()
                                    elif split_cmd[0].lower() == 'br':
                                        query.CaseID_BR=query.synthetic_field_str()
                                    elif split_cmd[0].lower() == 'all':
                                        query.CaseID_6W=query.synthetic_field_str()
                                        query.CaseID_LD=query.synthetic_field_str()
                                        query.CaseID_BR=query.synthetic_field_str()
                                else:
                                    if split_cmd[0].lower() == '6w':
                                        query.CaseID_6W=ex
                                    elif split_cmd[0].lower() == 'ld':
                                        query.CaseID_LD=ex
                                    elif split_cmd[0].lower() == 'br':
                                        query.CaseID_BR=ex
                                    elif split_cmd[0].lower() == 'all':
                                        query.CaseID_6W=ex
                                        query.CaseID_LD=ex
                                        query.CaseID_BR=ex
                                session.commit()
                                session.flush()
                                session.refresh(query)
                                print(f"""
    Name: {query.Name}
    Barcode: {query.Barcode}
    Code: {query.Code}
    EntryId: {query.EntryId}
    CaseId 6W: {query.CaseID_6W}
    CaseId LD: {query.CaseID_LD}
    CaseId BR: {query.CaseID_BR}
    """)
                elif len(split_cmd)==2:
                    with Session(self.engine) as session:
                        query=session.query(Entry).filter(Entry.EntryId==int(split_cmd[1]))
                        r=query.first()
                        if r:
                            if split_cmd[0].lower() == '6w':
                                print(r.CaseID_6W)
                            elif split_cmd[0].lower() == 'ld':
                                print(r.CaseID_LD)
                            elif split_cmd[0].lower() == 'br':
                                print(r.CaseID_BR)
                                #self.CaseID_BR=CaseID_BR
                                #self.CaseID_LD=CaseID_LD
                                #self.CaseID_6W=CaseID_6W
                        else:
                            print(f"{Fore.dark_goldenrod}No Such Item!{Style.reset}")
                else:
                    print(self.helpText_caseIds)


    helpText_tags=f'''{prefix_text}
{Fore.green_yellow}$mode[=|R,+,-],$TAG_TEXT,$fieldname,$id|$code|$barcode|$fieldData_to_id{Style.reset}
{Fore.cyan}=|R{Style.reset} -> {Fore.yellow}{Style.bold}set Tag to $TAG_TEXT{Style.reset}
{Fore.cyan}+{Style.reset} -> {Fore.yellow}{Style.bold}add $TAG_TEXT to Tag{Style.reset}
{Fore.cyan}-{Style.reset} -> {Fore.yellow}{Style.bold}remove $TAG_TEXT from Tag{Style.reset}
{Fore.cyan}s|search{Style.reset} -> {Fore.yellow}{Style.bold}search for items containing Tag{Style.reset}
{Fore.cyan}l|list{Style.reset} -> {Fore.yellow}{Style.bold}List All Tags{Style.reset}
{Fore.light_red}{Style.bold}This performs operations on all results found without confirmation for mass tag-edits{Style.reset}
{Fore.cyan}ba|bta|bulk_tag_add{Style.reset} -> {Fore.yellow}{Style.bold}Bulk add Tags to {Fore.light_magenta}{Style.underline}#code{Style.reset}
{Fore.cyan}br|btr|bulk_tag_rem{Style.reset} -> {Fore.yellow}{Style.bold}Bulk remove Tags from {Fore.light_magenta}{Style.underline}#code{Style.reset}
{Fore.red}{Style.bold}reset_all_tags|clear_all_tags -> {Fore.yellow}{Style.underline} reset all tags to []{Style.reset}
    '''
    def editTags(self):
        while True:
            #cmd=input("Do What[help]?: ")
            #PROMPT
            def mkT(text,self):
                return text
            cmd=Prompt.__init2__(None,func=mkT,ptext='Do What[help]?',helpText=self.helpText_tags,data=self)
            if not cmd:
                break

            if cmd.lower() in ['l','list']:
                with Session(self.engine) as session:
                    tags=[]
                    allTags=session.query(Entry).all()
                    for i in allTags:
                        if i.Tags and i.Tags != '':
                            try:
                                tl=json.loads(i.Tags)
                                for t in tl:
                                    if t not in tags:
                                        tags.append(t)
                            except Exception as e:
                                print(e)
                    tagCt=len(tags)
                    for num,t in enumerate(tags):
                        print(f"{Fore.green}{num}{Style.reset}/{Fore.light_red}{tagCt-1}{Style.reset} -> {Fore.light_magenta}'{Style.reset}{Fore.grey_70}{t}{Style.reset}{Fore.light_magenta}'{Style.reset}")
            elif cmd.lower() in ['s','search']:
                def mkT(text,self):
                    return text
                tag=Prompt.__init2__(None,func=mkT,ptext='Tag[help]?',helpText=self.helpText_tags,data=self)
                if not tag:
                    break
               
                with Session(self.engine) as session:
                    results=session.query(Entry).all()
                    ct=len(results)
                    t=[]
                    for num,r in enumerate(results):
                        #print(r.Tags)
                        try:
                            if r.Tags not in ['',None]:

                                if tag in list(json.loads(r.Tags)):
                                    t.append(r)
                        except Exception as e:
                            pass
                    for num,rr in enumerate(t):
                        print(f"{Fore.green}{num}{Style.reset}/{Fore.light_red}{ct}{Style.reset} -> {rr}")
                    print(f"{Fore.light_yellow}there was/were {Style.reset}{Fore.light_blue}{len(t)} Results.{Style.reset}")
                    inlist=Prompt.__init2__(None,func=mkT,ptext='Set Results to Have InList=True[help]?',helpText=self.helpText_tags,data=self)
                    if not inlist:
                        break
                    if inlist.lower() in ['y','yes']:
                        ct2=len(t)
                        for num,x in enumerate(t):
                            x.InList=True
                            print(f"{Fore.light_green}{num}{r.EntryId}={Style.reset}{Fore.light_yellow}{r.InList}{Style.reset}/{Fore.light_red}{ct2}{Style.reset}")
                            if num%50 ==0:
                                session.commit()
                        session.commit()
            elif cmd.lower() in ['ba','bulk_tag_add']:
                while True:
                    try:
                        with Session(self.engine) as session:
                            query=session.query(Entry)
                            def mkT(text,self):
                                return text
                            tag=Prompt.__init2__(None,func=mkT,ptext="Tag",helpText="Tag to add to code")
                            while True:
                                try:
                                    #code=Prompt.__init2__(None,func=mkT,ptext="Code|Barcode",helpText=f"Code|Barcode to add Tag:'{tag}' to.")
                                    #if code in [None,]:
                                    #    break
                                    def addTag(session,entry,tag):
                                        try:
                                            old=list(json.loads(entry.Tags))
                                            if tag not in old:
                                                old.append(tag)
                                            entry.Tags=json.dumps(old)
                                        except Exception as e:
                                            print(e)
                                            entry.Tags=json.dumps([tag,])
                                        session.commit()
                                        session.flush()
                                        session.refresh(entry)
                                        
                                    def e_do(self,code,tag):
                                        with Session(self.engine) as session:
                                            try:
                                                code=int(code)
                                                query=session.query(Entry).filter(Entry.EntryId==code)
                                                results=query.all()
                                                ct=len(results)
                                                if len(results)==0:
                                                    print(f"{Fore.light_red}No Entry was found to match that code '{code}'{Style.reset}")
                                                for num,r in enumerate(results):
                                                    if num%2==0:
                                                        colorEntry=Style.bold
                                                    else:
                                                        colorEntry=Fore.grey_70+Style.underline
                                                    addTag(session,r,tag)
                                                    session.refresh(r)
                                                    compound=f'{colorEntry}{r.Name}|{r.Barcode}|{r.Code}|{r.EntryId}|{r.Tags}{Style.reset}'
                                                    if num == 0:
                                                        color1=Fore.light_green
                                                    elif num > 0 and num%2==0:
                                                        color1=Fore.green_yellow
                                                    elif num > 0 and num%2!=0:
                                                        color1=Fore.dark_goldenrod
                                                    elif num+1 == ct:
                                                        color1=Fore.light_red
                                                    print(f"{color1}{num}{Style.reset}/{Fore.red}{ct-1}{Style.reset} {compound}")
                                            except Exception as e:
                                                print(e)

                                    def b_do(self,code,tag):
                                        with Session(self.engine) as session:
                                            query=session.query(Entry).filter(or_(Entry.Barcode==code,Entry.Barcode.icontains(code)))
                                            results=query.all()
                                            ct=len(results)
                                            if len(results)==0:
                                                print(f"{Fore.light_red}No Entry was found to match that code '{code}'{Style.reset}")                                            
                                            for num,r in enumerate(results):
                                                if num%2==0:
                                                    colorEntry=Style.bold
                                                else:
                                                    colorEntry=Fore.grey_70+Style.underline
                                                addTag(session,r,tag)
                                                session.refresh(r)
                                                compound=f'{colorEntry}{r.Name}|{r.Barcode}|{r.Code}|{r.EntryId}|{r.Tags}{Style.reset}'
                                                if num == 0:
                                                    color1=Fore.light_green
                                                elif num > 0 and num%2==0:
                                                    color1=Fore.green_yellow
                                                elif num > 0 and num%2!=0:
                                                    color1=Fore.dark_goldenrod
                                                elif num+1 == ct:
                                                    color1=Fore.light_red
                                                print(f"{color1}{num}{Style.reset}/{Fore.red}{ct-1}{Style.reset} {compound}")

                                    def c_do(self,code,tag):
                                        with Session(self.engine) as session:
                                            query=session.query(Entry).filter(or_(Entry.Code==code,Entry.Code.icontains(code)))
                                            results=query.all()
                                            ct=len(results)
                                            if len(results)==0:
                                                print(f"{Fore.light_red}No Entry was found to match that code '{code}'{Style.reset}")
                                            for num,r in enumerate(results):
                                                if num%2==0:
                                                    colorEntry=Style.bold
                                                else:
                                                    colorEntry=Fore.grey_70+Style.underline
                                                addTag(session,r,tag)
                                                session.refresh(r)
                                                compound=f'{colorEntry}{r.Name}|{r.Barcode}|{r.Code}|{r.EntryId}|{r.Tags}{Style.reset}'
                                                if num == 0:
                                                    color1=Fore.light_green
                                                elif num > 0 and num%2==0:
                                                    color1=Fore.green_yellow
                                                elif num > 0 and num%2!=0:
                                                    color1=Fore.dark_goldenrod
                                                elif num+1 == ct:
                                                    color1=Fore.light_red
                                                print(f"{color1}{num}{Style.reset}/{Fore.red}{ct-1}{Style.reset} {compound}")
                                    def do(self,code,tag):
                                        with Session(self.engine) as session:
                                            query=session.query(Entry).filter(or_(Entry.Code==code,Entry.Barcode==code,Entry.Code.icontains(code),Entry.Barcode.icontains(code)))
                                            results=query.all()
                                            ct=len(results)
                                            if len(results)==0:
                                                print(f"{Fore.light_red}No Entry was found to match that code '{code}'{Style.reset}")
                                            for num,r in enumerate(results):
                                                if num%2==0:
                                                    colorEntry=Style.bold
                                                else:
                                                    colorEntry=Fore.grey_70+Style.underline
                                                addTag(session,r,tag)
                                                compound=f'{colorEntry}{r.Name}|{r.Barcode}|{r.Code}|{r.EntryId}|{r.Tags}{Style.reset}'
                                                if num == 0:
                                                    color1=Fore.light_green
                                                elif num > 0 and num%2==0:
                                                    color1=Fore.green_yellow
                                                elif num > 0 and num%2!=0:
                                                    color1=Fore.dark_goldenrod
                                                elif num+1 == ct:
                                                    color1=Fore.light_red
                                                print(f"{color1}{num}{Style.reset}/{Fore.red}{ct-1}{Style.reset} {compound}")
                                                    
                                    ex={
                                        'delim':'.',
                                        'e_do':lambda code,tag=tag,self=self:e_do(self,code,tag),
                                        'c_do':lambda code,tag=tag,self=self:c_do(self,code,tag),
                                        'b_do':lambda code,tag=tag,self=self:b_do(self,code,tag),
                                        'do':lambda code,tag=tag,self=self:do(self,code,tag)
                                    }
                                    status=Prompt(func=prefix_filter,ptext="Code|Barcode|(e|B|c).$code) ",helpText="Code|Barcode|EntryId to have tag applied to prefix will use the specified field e. == EntryID, c. == Code, B. == Barcode.",data=ex)
                                    if status.status == False:
                                        break   
                                except Exception as e:
                                    print(e)

                        break
                    except Exception as e:
                        print(e)
            elif cmd.lower() in ['br','btr','bulk_tag_rem']:
                while True:
                    try:
                        with Session(self.engine) as session:
                            query=session.query(Entry)
                            def mkT(text,self):
                                return text
                            tag=Prompt.__init2__(None,func=mkT,ptext="Tag",helpText="Tag to remove from code")
                            while True:
                                try:
                                    #code=Prompt.__init2__(None,func=mkT,ptext="Code|Barcode",helpText=f"Code|Barcode to add Tag:'{tag}' to.")
                                    #if code in [None,]:
                                    #    break
                                    def remTag(session,entry,tag):
                                        try:
                                            old=list(json.loads(entry.Tags))
                                            if tag not in old:
                                                return
                                            tmp=[]
                                            for t in old:
                                                if t != tag:
                                                    tmp.append(t)
                                            entry.Tags=json.dumps(tmp)
                                        except Exception as e:
                                            print(e)
                                            entry.Tags=json.dumps([])
                                        session.commit()
                                        session.flush()
                                        session.refresh(entry)

                                    def e_do(self,code,tag):
                                        with Session(self.engine) as session:
                                            try:
                                                code=int(code)
                                                query=session.query(Entry).filter(Entry.EntryId==code)
                                                results=query.all()
                                                ct=len(results)
                                                if len(results)==0:
                                                    print(f"{Fore.light_red}No Entry was found to match that code '{code}'{Style.reset}")
                                                for num,r in enumerate(results):
                                                    results=query.all()
                                                    if num%2==0:
                                                        colorEntry=Style.bold
                                                    else:
                                                        colorEntry=Fore.grey_70+Style.underline
                                                    remTag(session,r,tag)
                                                    session.refresh(r)
                                                    compound=f'{colorEntry}{r.Name}|{r.Barcode}|{r.Code}|{r.EntryId}|{r.Tags}{Style.reset}'
                                                    if num == 0:
                                                        color1=Fore.light_green
                                                    elif num > 0 and num%2==0:
                                                        color1=Fore.green_yellow
                                                    elif num > 0 and num%2!=0:
                                                        color1=Fore.dark_goldenrod
                                                    elif num+1 == ct:
                                                        color1=Fore.light_red
                                                    print(f"{color1}{num}{Style.reset}/{Fore.red}{ct-1}{Style.reset} {compound}")
                                                    
                                            except Exception as e:
                                                print(e)

                                    def b_do(self,code,tag):
                                        with Session(self.engine) as session:
                                            query=session.query(Entry).filter(or_(Entry.Barcode==code,Entry.Barcode.icontains(code)))
                                            results=query.all()
                                            ct=len(results)
                                            if len(results)==0:
                                                print(f"{Fore.light_red}No Entry was found to match that code '{code}'{Style.reset}")                                            
                                            for num,r in enumerate(results):
                                                if num%2==0:
                                                    colorEntry=Style.bold
                                                else:
                                                    colorEntry=Fore.grey_70+Style.underline
                                                remTag(session,r,tag)
                                                session.refresh(r)
                                                compound=f'{colorEntry}{r.Name}|{r.Barcode}|{r.Code}|{r.EntryId}|{r.Tags}{Style.reset}'
                                                if num == 0:
                                                    color1=Fore.light_green
                                                elif num > 0 and num%2==0:
                                                    color1=Fore.green_yellow
                                                elif num > 0 and num%2!=0:
                                                    color1=Fore.dark_goldenrod
                                                elif num+1 == ct:
                                                    color1=Fore.light_red
                                                print(f"{color1}{num}{Style.reset}/{Fore.red}{ct-1}{Style.reset} {compound}")
                                                    
                                                #print(f"{Fore.light_yellow}{num}{Style.reset}/{Fore.light_red}{ct}{Style.reset} -> {r}")
                                                #remTag(session,r,tag)

                                    def c_do(self,code,tag):
                                        with Session(self.engine) as session:
                                            query=session.query(Entry).filter(or_(Entry.Code==code,Entry.Code.icontains(code)))
                                            results=query.all()
                                            ct=len(results)
                                            if len(results)==0:
                                                print(f"{Fore.light_red}No Entry was found to match that code '{code}'{Style.reset}")
                                            for num,r in enumerate(results):
                                                if num%2==0:
                                                    colorEntry=Style.bold
                                                else:
                                                    colorEntry=Fore.grey_70+Style.underline
                                                remTag(session,r,tag)
                                                session.refresh(r)
                                                compound=f'{colorEntry}{r.Name}|{r.Barcode}|{r.Code}|{r.EntryId}|{r.Tags}{Style.reset}'
                                                if num == 0:
                                                    color1=Fore.light_green
                                                elif num > 0 and num%2==0:
                                                    color1=Fore.green_yellow
                                                elif num > 0 and num%2!=0:
                                                    color1=Fore.dark_goldenrod
                                                elif num+1 == ct:
                                                    color1=Fore.light_red
                                                print(f"{color1}{num}{Style.reset}/{Fore.red}{ct-1}{Style.reset} {compound}")
                                                    
                                    def do(self,code,tag):
                                        with Session(self.engine) as session:
                                            query=session.query(Entry).filter(or_(Entry.Code==code,Entry.Barcode==code,Entry.Code.icontains(code),Entry.Barcode.icontains(code)))
                                            results=query.all()
                                            ct=len(results)
                                            if len(results)==0:
                                                print(f"{Fore.light_red}No Entry was found to match that code '{code}'{Style.reset}")
                                            for num,r in enumerate(results):
                                                if num%2==0:
                                                    colorEntry=Style.bold
                                                else:
                                                    colorEntry=Fore.grey_70+Style.underline
                                                remTag(session,r,tag)
                                                session.refresh(r)
                                                compound=f'{colorEntry}{r.Name}|{r.Barcode}|{r.Code}|{r.EntryId}|{r.Tags}{Style.reset}'
                                                if num == 0:
                                                    color1=Fore.light_green
                                                elif num > 0 and num%2==0:
                                                    color1=Fore.green_yellow
                                                elif num > 0 and num%2!=0:
                                                    color1=Fore.dark_goldenrod
                                                elif num+1 == ct:
                                                    color1=Fore.light_red
                                                print(f"{color1}{num}{Style.reset}/{Fore.red}{ct-1}{Style.reset} {compound}")
                                                    
                                    ex={
                                        'delim':'.',
                                        'e_do':lambda code,tag=tag,self=self:e_do(self,code,tag),
                                        'c_do':lambda code,tag=tag,self=self:c_do(self,code,tag),
                                        'b_do':lambda code,tag=tag,self=self:b_do(self,code,tag),
                                        'do':lambda code,tag=tag,self=self:do(self,code,tag)
                                    }
                                    status=Prompt(func=prefix_filter,ptext="Code|Barcode|(e|B|c).$code) ",helpText="Code|Barcode|EntryId to have tag remove from (prefix will use the specified field e. == EntryID, c. == Code, B. == Barcode.)",data=ex)
                                    if status.status == False:
                                        break   
                                except Exception as e:
                                    print(e)

                        break
                    except Exception as e:
                        print(e)
            elif cmd.lower() in ['reset_all_tags','clear_all_tags',]:
                with Session(self.engine) as session:
                    query=session.query(Entry)
                    results=query.all()
                    ct=len(results)
                    if ct == 0:
                        print(f"{Fore.red}No Entry's with Tags to reset!{Style.reset}")
                    for num,r in enumerate(results):
                        if num%2==0:
                            colorEntry=Style.bold
                        else:
                            colorEntry=Fore.grey_70+Style.underline
                        compound=f'{colorEntry}{r.Name}|{r.Barcode}|{r.Code}|{r.EntryId}|{r.Tags}{Style.reset}'
                        if num == 0:
                            color1=Fore.light_green
                        elif num > 0 and num%2==0:
                            color1=Fore.green_yellow
                        elif num > 0 and num%2!=0:
                            color1=Fore.dark_goldenrod
                        elif num+1 == ct:
                            color1=Fore.light_red

                        print(f"{color1}{num}{Style.reset}/{Fore.red}{ct-1}{Style.reset} {compound}")
            else:
                split_cmd=cmd.split(",")
                if len(split_cmd) == 4:
                    #$mode,$search_fieldname,$EntryId,$tag
                    mode=split_cmd[0]
                    tag=[split_cmd[1],] 
                    search_fieldname=split_cmd[2]
                    eid=int(split_cmd[3])
                    with Session(self.engine) as session:
                        result=session.query(Entry).filter(Entry.__dict__.get(search_fieldname)==eid).all()
                        for num,r in enumerate(result):
                            msg=''
                            if r.Tags == '':
                                 r.Tags=json.dumps(list(tag))
                            
                            if mode in ['=','r','R']:
                                r.Tags=json.dumps(list(tag))
                            elif mode == '+':
                                try:
                                    old=json.loads(r.Tags)
                                    if tag[0] not in old:
                                        old.append(tag[0])
                                        r.Tags=json.dumps(old)
                                    else:
                                        msg=f"{Fore.light_yellow}Tag is Already Applied Nothing will be Done!{Style.reset}"
                                except Exception as e:
                                    print(e)
                            elif mode == '-':
                                try:
                                    old=json.loads(r.Tags)
                                    if tag[0] in old:
                                        i=old.index(tag[0])
                                        old.pop(i)
                                        r.Tags=json.dumps(old)
                                    else:
                                        msg=f"{Fore.light_red}No Such Tag in Item...{Fore.light_yellow} Nothing will be done!{Style.reset}"
                                except Exception as e:
                                    print(e)
                                

                            
                            session.commit()
                            session.flush()
                            session.refresh(r)
                            print(r)
                            print(msg)
                else:
                    print(self.helpText_tags)


    def setName(self):
        with Session(self.engine) as session:
            def mkT(text,self):
                    return text
            code=Prompt.__init2__(None,func=mkT,ptext='Code|Barcode[help]?',helpText='',data=self)
            if not code:
                return
            
            value=Prompt.__init2__(None,func=mkT,ptext='Name[help]?',helpText='',data=self)
            if not value:
                return
           
            result=session.query(Entry).filter(or_(Entry.Barcode==code,Entry.Code==code)).first()
            if result:
                result.Name=value
                session.commit()
                session.flush()
                session.refresh(result)
                print(result)
            else:
                print(f"{Fore.red}{Style.bold}No Such Item Identified by '{code}'{Style.reset}")

    def list_total(self):
        with Session(self.engine) as session:
            results=session.query(Entry).filter(Entry.InList==True).all()
            ct=len(results)
            total=0
            total_case=0
            total_units=0
            total_units_br=0
            for num,r in enumerate(results):
                print(f"{Fore.green}{num}{Style.reset}/{Fore.light_red}{ct-1}{Style.reset} -> {r}")
                total+=r.total_value(CaseMode=False)
                total_case+=r.total_value(CaseMode=True)
                total_units+=r.total_units()
                total_units_br+=r.total_units(BackRoom=False)
            #print(total_units,total_units_br)
            print(f"""
{Fore.light_green}Total By Units: ${Fore.light_red}{total}{Style.reset}{Fore.green_yellow} for{Fore.light_red} {total_units} w/BackRoom{Fore.light_green} | {total_units_br} {Fore.light_magenta}wo/BackRoom{Style.reset}
{Fore.light_green}Total By Case: ${Fore.light_red}{total_case}{Style.reset}{Fore.green_yellow} for{Fore.light_red} {total_units} w/BackRoom{Fore.light_green} | {total_units_br} {Fore.light_magenta}wo/BackRoom{Style.reset} 
""")

    def __init__(self,engine,parent):
        self.engine=engine
        self.parent=parent
        self.special=['Tags','ALT_Barcode','DUP_Barcode','CaseID_6W','CaseID_BR','CaseID_LD','Facings']
        self.valid_fields=['Shelf',
        'BackRoom',
        'Display_1',
        'Display_2',
        'Display_3',
        'Display_4',
        'Display_5',
        'Display_6',
        'ALT_Barcode',
        'DUP_Barcode',
        'CaseID_BR',
        'CaseID_LD',
        'CaseID_6W',
        'Tags',
        'Facings',
        'SBX_WTR_DSPLY',
        'SBX_CHP_DSPLY',
        'SBX_WTR_KLR',
        'FLRL_CHP_DSPLY',
        'FLRL_WTR_DSPLY',
        'WD_DSPLY',
        'CHKSTND_SPLY',
        ]
        '''
        ALT_Barcode=Column(String)
        DUP_Barcode=Column(String)
        CaseID_BR=Column(String)
        CaseID_LD=Column(String)
        CaseID_6W=Column(String)
        Tags=Column(String)
        Facings=Column(Integer)
        SBX_WTR_DSPLY=Column(Integer)
        SBX_CHP_DSPLY=Column(Integer)
        SBX_WTR_KLR=Column(Integer)
        FLRL_CHP_DSPLY=Column(Integer)
        FLRL_WTR_DSPLY=Column(Integer)
        WD_DSPLY=WD_DSPLY=Column(Integer)
        CHKSTND_SPLY=CHKSTND_SPLY=Column(Integer)
        '''
        #self.display_field("Shelf")
        self.options={
                '1':{
                    'cmds':['q','quit','#1'],
                    'desc':"quit program",
                    'exec':lambda: exit("user quit!"),
                    },
                '2':{
                    'cmds':['b','back','#2'],
                    'desc':'go back menu if any',
                    'exec':None
                    },
                }
        #autogenerate duplicate functionality for all valid fields for display
        count=3
        for entry in self.valid_fields:
            self.options[entry]={
                    'cmds':["#"+str(count),f"ls {entry}"],
                    'desc':f'list needed @ {entry}',
                    'exec':lambda self=self,entry=entry: self.display_field(f"{entry}"),
                    }
            count+=1
        #setoptions
        #self.setFieldInList("Shelf")
        for entry in self.valid_fields:
            self.options[entry+"_set"]={
                    'cmds':["#"+str(count),f"set {entry}"],
                    'desc':f'set needed @ {entry}',
                    'exec':lambda self=self,entry=entry: self.setFieldInList(f"{entry}"),
                    }
            count+=1
        self.options["lu"]={
                    'cmds':["#"+str(count),f"lookup","lu","check","ck"],
                    'desc':f'get total for valid fields',
                    'exec':lambda self=self,entry=entry: self.getTotalwithBreakDownForScan(),
                    }
        count+=1
        self.options["setName"]={
                    'cmds':["#"+str(count),f"setName","sn"],
                    'desc':f'set name for item by barcode!',
                    'exec':lambda self=self,entry=entry: self.setName(),
                    }
        count+=1
        self.options["setListQty"]={
                    'cmds':["#"+str(count),f"setListQty","slq"],
                    'desc':f'set ListQty for Values not wanted to be included in totals.',
                    'exec':lambda self=self: self.setFieldInList("ListQty",load=True),
                    }
        count+=1
        self.options["lsListQty"]={
                    'cmds':["#"+str(count),f"lsListQty","ls-lq"],
                    'desc':f'show ListQty for Values not wanted to be included in totals.',
                    'exec':lambda self=self: self.display_field("ListQty",load=True),
                    }
        count+=1
        self.options["listTotal"]={
                    'cmds':["#"+str(count),f"listTotal","list_total"],
                    'desc':f'show list total value.',
                    'exec':lambda self=self: self.list_total(),
                    }
        count+=1
        self.options["lus"]={
                    'cmds':["#"+str(count),f"lookup_short","lus","lu-","check","ck-","ls"],
                    'desc':f'get total for valid fields short view',
                    'exec':lambda self=self,entry=entry: self.getTotalwithBreakDownForScan(short=True),
                    }
        count+=1
        self.options["b1"]={
                    'cmds':["#"+str(count),f"barcode_first","b1"],
                    'desc':f'list mode where barcode is asked first',
                    'exec':lambda self=self: self.setFieldInList(None,load=True),
                    }
        count+=1
        self.options["el2e"]={
                    'cmds':["#"+str(count),f"export-list-2-excel","el2e"],
                    'desc':f'export fields {self.exportList2Excel(fields=True)} to Excel file',
                    'exec':lambda self=self: self.exportList2Excel(),
                    }
        count+=1
        self.options["formula"]={
                    'cmds':["#"+str(count),f"formula","eval","calc"],
                    'desc':f'solve an equation',
                    'exec':lambda self=self: self.evaluateFormula(),
                    }
        count+=1


        while True:
            def mkT(text,self):
                return text
            command=Prompt.__init2__(None,func=mkT,ptext='Do What[help/??/?]',helpText=self.parent.help(print_no=True),data=self)
            if not command:
                break
            #command=input(f"{Style.bold}{Fore.green}do what[??/?]:{Style.reset} ")
            if self.parent != None and self.parent.Unified(command):
                print("ran a Unified CMD")
            elif command == "??":
                for num,option in enumerate(self.options):
                    color=Fore.dark_goldenrod
                    color1=Fore.cyan
                    if (num%2)==0:
                        color=Fore.green_yellow
                        color1=Fore.magenta
                    print(f"{color}{self.options[option]['cmds']}{Style.reset} - {color1}{self.options[option]['desc']}{Style.reset}")
            else:
                for option in self.options:
                    if self.options[option]['exec'] != None and command.lower() in self.options[option]['cmds']:
                        self.options[option]['exec']()
                    elif self.options[option]['exec'] == None and command.lower() in self.options[option]['cmds']:
                        return
    
    def evaluateFormula(self):
        while True:
            try:
                accro=Style.bold+Style.underline+Fore.light_red
                p1=Fore.light_magenta
                p2=Fore.light_yellow
                p3=Fore.light_green
                p4=Fore.cyan
                p5=Fore.sea_green_1a
                p6=Fore.green_yellow
                p7=Fore.dark_goldenrod
                symbol=Fore.magenta
                helpText=f'''
{accro}Operator Symbol -> {symbol}()|**|*|/|+|-{Style.reset}
{accro}CVTR.convert(value,fromUnite,toUnit) -> {symbol}Convert a value from one to another{Style.reset}
{accro}datetime()+|-datetime()|timedelta() -> {symbol}Add or Subtract datetimes{Style.reset}
{accro}if you know a tool in pandas use pd, or numpy use np ->{symbol}module support for advanced math operations on a single line{Style.reset}
{accro}PEMDAS{Style.reset} - {p1}Please {p2}Excuse {p4}My {p5}Dear {p6}Aunt {p7}Sallie{Style.reset}
{accro}PEMDAS{Style.reset} - {p1}{symbol}({Style.reset}{p1}Parantheses{symbol}){Style.reset} {p3}Exponents{symbol}** {p4}Multiplication{symbol}* {p5}Division{symbol}/ {p6}Addition{symbol}+ {p7}Subtraction{symbol}-{Style.reset}
                '''
                def mkValue(text,self):
                    try:
                        CVTR=UnitRegistry()
                        return eval(text)
                    except Exception as e:
                        print(e)
                formula=Prompt.__init2__(None,func=mkValue,ptext="Type|Tap your equation and remember PEMDAS",helpText=helpText,data=self)
                if formula in [None,]:
                    break
                print(formula)
            except Exception as e:
                print(e)




if __name__ == "__main__":
    TasksMode(parent=None,engine=ENGINE)
