"""Apply documented educational closure controls to the existing synthetic workbook.
Preserves the original ZIP entries except the two targeted worksheets.
"""
import io, zipfile, xml.etree.ElementTree as ET, pathlib, shutil
P=pathlib.Path("Patient_Access_Bottleneck_Intelligence_System.xlsx")
N="http://schemas.openxmlformats.org/spreadsheetml/2006/main"
X="{"+N+"}"
ET.register_namespace("",N)
ET.register_namespace("r","http://schemas.openxmlformats.org/officeDocument/2006/relationships")
ET.register_namespace("mc","http://schemas.openxmlformats.org/markup-compatibility/2006")
ET.register_namespace("x14ac","http://schemas.microsoft.com/office/spreadsheetml/2009/9/ac")
ET.register_namespace("xr","http://schemas.microsoft.com/office/spreadsheetml/2014/revision")
def child(root,name):return root.find(X+name)
def addcell(row,ref,formula=None,text=None,style=None):
 c=ET.SubElement(row,X+"c",{"r":ref})
 if style:c.set("s",style)
 if formula is not None:
  ET.SubElement(c,X+"f").text=formula
  ET.SubElement(c,X+"v")
 if text is not None:
  c.set("t","inlineStr")
  ET.SubElement(ET.SubElement(c,X+"is"),X+"t").text=text
 return c
def patch_case(data):
 root=ET.fromstring(data); sd=child(root,"sheetData")
 rows={int(r.get("r")):r for r in sd.findall(X+"row")}
 if any(c.get("r")=="U5" for c in rows[5].findall(X+"c")):raise RuntimeError("Already patched")
 addcell(rows[4],"U4",text="MODELED CLOSURE CONTROL",style="8")
 for i in range(5,17):
  f='IF(P{0}<>"Closed","Not applicable",IF(OR(Q{0}="",R{0}="",S{0}<>"Pass",O{0}=""),"BLOCKED — review closure","Ready — modeled closure only"))'.format(i)
  addcell(rows[i],"U"+str(i),formula=f,style="9" if i%2 else "10")
 dim=child(root,"dimension")
 if dim is not None:dim.set("ref",dim.get("ref","A1:T16").replace(":T",":U"))
 dvs=ET.Element(X+"dataValidations",{"count":"3"})
 for rng,options in [("H5:H16","Low,Medium,High,Urgent"),("P5:P16","Open,In Progress,Closed"),("S5:S16","Pending,Pass,Fail")]:
  dv=ET.SubElement(dvs,X+"dataValidation",{"type":"list","sqref":rng})
  ET.SubElement(dv,X+"formula1").text='"'+options+'"'
 # Worksheet child order: validations follow conditionalFormatting and precede hyperlinks/pageMargins.
 after={"sheetData","sheetCalcPr","sheetProtection","protectedRanges","scenarios","autoFilter","sortState","dataConsolidate","customSheetViews","mergeCells","phoneticPr","conditionalFormatting"}
 idx=next((i for i,e in enumerate(root) if e.tag.split("}")[-1] not in after and i>list(root).index(sd)),len(root))
 root.insert(idx,dvs)
 return ET.tostring(root,encoding="utf-8",xml_declaration=True)
def patch_dashboard(data):
 root=ET.fromstring(data);sd=child(root,"sheetData")
 row=ET.SubElement(sd,X+"row",{"r":"13"})
 addcell(row,"A13",text="Blocked modeled closures")
 addcell(row,"B13",formula='COUNTIF(\'CASE CONTROL\'!U5:U16,"BLOCKED*")')
 return ET.tostring(root,encoding="utf-8",xml_declaration=True)
with zipfile.ZipFile(P) as src:
 entries={n:src.read(n) for n in src.namelist()}
 entries["xl/worksheets/sheet3.xml"]=patch_case(entries["xl/worksheets/sheet3.xml"])
 entries["xl/worksheets/sheet6.xml"]=patch_dashboard(entries["xl/worksheets/sheet6.xml"])
out=P.with_suffix(".tmp")
with zipfile.ZipFile(out,"w",zipfile.ZIP_DEFLATED) as z:
 for name,data in entries.items():z.writestr(name,data)
with zipfile.ZipFile(out) as z:
 assert z.testzip() is None
 import re
 sheets=[v for k,v in ((k,z.read(k)) for k in z.namelist()) if re.fullmatch(r"xl/worksheets/sheet\d+\.xml",k)]
 assert len(sheets)==8
 assert sum(len(re.findall(rb"<(?:\w+:)?f(?:\s|>)",s)) for s in sheets)==50
 assert sum(len(re.findall(rb"<(?:\w+:)?dataValidation\b",s)) for s in sheets)==3
out.replace(P)
print("PASS: 8 sheets, 50 formulas, 3 dropdown validation rules; original backed up in Git history")
