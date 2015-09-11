import glob

import zipfile

count = 0
for file in glob.glob("hoc_combos_syn.1_0_10.allzips/L*.zip"):
    print(file)
    zip_ref = zipfile.ZipFile(file, 'r')
    zip_ref.extractall('.')
    zip_ref.close()
    
    
    count+=1
    
    
print("\n  Extracted %i zips\n"%count)
