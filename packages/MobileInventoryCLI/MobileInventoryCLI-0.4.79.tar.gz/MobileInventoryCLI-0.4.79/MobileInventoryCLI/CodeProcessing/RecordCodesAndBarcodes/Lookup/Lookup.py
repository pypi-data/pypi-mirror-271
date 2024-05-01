from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.DB.db import *
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.DB.Prompt import *
from colored import Style,Fore,Back

class Lookup:
	def __init__(self,engine,tbl):
		self.engine=engine
		self.tbl=tbl
		self.cmds={
		'1':{
			'cmds':['q','quit'],
			'exec':lambda self=self:exit("user quit!"),
			'desc':f'{Fore.light_red}Quit the program!{Style.reset}'
		},
		'2':{
			'cmds':['b','back'],
			'exec':None,
			'desc':f'{Fore.light_red}Go Back a Menu!{Style.reset}'
		},
		'3':{
			'cmds':['3','sbc','search_bc',],
			'exec':self.search,
			'desc':f'{Fore.light_blue}Lookup Codes by Barcode|Code{Style.reset}',
		},
		'4l':{
			'cmds':['4l','search_auto_long','sal'],
			'exec':self.SearchAuto,
			'desc':f'{Fore.light_blue}Search For Product by Name,Barcode,Code,Note,Size {Fore.cyan}*Note: these are text only searches, for numeric use Task Mode with the "s" command{Style.reset}'
		},
		'4s':{
			'cmds':['4s','search_auto_short','sas'],
			'exec':lambda self=self:self.SearchAuto(short=True),
			'desc':f'{Fore.light_blue}Search For Product by Name,Barcode,Code,Note,Size {Fore.cyan}*Note: these are text only searches, for numeric use Task Mode with the "s" command{Style.reset}'
		},
		'5':{
			'cmds':['5','sm','search_manual'],
			'exec':self.SearchManual,
			'desc':f'{Fore.light_blue}Search For Product by Field {Fore.cyan}*Note: these are text only searches, for numeric use Task Mode with the "s" command{Style.reset}'
		}

		}
		while True:
			for k in self.cmds:
				print(f"{Fore.medium_violet_red}{self.cmds[k]['cmds']}{Style.reset} -{self.cmds[k]['desc']}")
			cmd=input("Do What: ")
			for i in self.cmds:
				if cmd.lower() in self.cmds[i]['cmds']:
					if cmd.lower() in self.cmds['2']['cmds']:
						return
					else:
						self.cmds[i]['exec']()
						break

	def SearchAuto(self,short=False):
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
						if not short:
							msg=f"{color_progress}{num}{Style.reset}/{Fore.light_red}{ct-1}{Style.reset} ->{r}"
						else:
							msg=f"{color_progress}{num}{Style.reset}/{Fore.light_red}{ct-1}{Style.reset} ->{r.seeShort()}"
						print(msg)
					print(f"{Fore.light_yellow}There are {Fore.light_red}{ct}{Fore.light_yellow} Total Results for search {Fore.medium_violet_red}'{stext}'{Style.reset}{Fore.light_yellow}.{Style.reset}")
					print(f"{Fore.light_red}Fields Searched in {Fore.cyan}{fields}{Style.reset}")
			except Exception as e:
				print(e)

	def SearchManual(self):
		while True:
			try:
				with Session(self.engine) as session:
					def mkT(text,self):
						return text
					fields=[i.name for i in Entry.__table__.columns if str(i.type) == "VARCHAR"]
					stext=Prompt.__init2__(None,func=mkT,ptext="Search[Field(s)]:",helpText="Search for Entry by field(s)",data=self)
					query=session.query(Entry)
					if not stext:
						break
					
					def mkTList(text,self):
						try:
							total=[]
							f=text.split(",")
							for i in f:
								if i in self:
									if i not in total:
										total.append(i)
							return total
						except Exception as e:
							return None
					to_search=f"{Fore.light_red}Fields available to Search in {Fore.cyan}{fields}{Style.reset}"
					sfields=Prompt.__init2__(None,func=mkTList,helpText=f"fields separated by a comma, or just a field from fields [Case-Sensitive]{to_search}",ptext="fields? ",data=fields)
					if not sfields:
						break


					q=[]
					
					for f in sfields:
						q.append(getattr(Entry,f).icontains(stext.lower()))

					query=query.filter(or_(*q))
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
					print(f"{Fore.light_red}Fields Searched in {Fore.cyan}{sfields}{Style.reset}")
			except Exception as e:
				print(e)

	def search(self):
		while True:
			try:
				code=input("Code to Search [q/b]: ")
				print(f"{Fore.green}{Style.underline}Lookup Initialized...{Style.reset}")
				if code.lower() in self.cmds['1']['cmds']:
					self.cmds['1']['exec']()
				elif code.lower() in self.cmds['2']['cmds']:
					break
				else:
					with Session(self.engine) as session:	
						query=session.query(Entry).filter(or_(Entry.Barcode==code,Entry.Code==code,Entry.ALT_Barcode==code))
						results=query.all()
						for num,r in enumerate(results):
							print(f'{Fore.red}{num}{Style.reset}/{Fore.green}{len(results)}{Style.reset} -> {r}')
						print(f"{Fore.cyan}There were {Fore.green}{Style.bold}{len(results)}{Style.reset} {Fore.cyan}results.{Style.reset}")
			except Exception as e:
				print(e)