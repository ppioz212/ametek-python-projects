import time
tic = time.time()
try:
    print('Work Order Shortage script has started running')
    import Work_order_shortage
    print('Work Order Shortage script has run without error')
    print('')
except:
    print("Work order shortage skipped due to error")
try:
    print('Part Number and WO Data update script has started running')
    import PN_and_WO_Data
    print('Part Number and WO Data script has run without error')
except:
    print("PN and WO data skipped due to error")
try:
    print('Master Part Data script has started running')
    import Master_Part_Data
    print('Master Part Data script has run without error')
except:
    print("Master Part Data skipped due to error")
try:
    print('Part Spec script has started running')
    import partspec
    print('Part Spec script has run without error')
except:
    print("Part spec data skipped due to error")
try:
    print('Work Order Mill data script has started running')
    import WO_Mill_Data
    print('Work Order Mill script has run without error')
except:
    print("Work Order Mill data skipped due to error")
try:
    print('Masters Ops data script has started running')
    import Masters_Ops_Data
    print('Master ops data script has run without error')
except:
    print("Masters Ops data skipped due to error")
try:
    print('Tinius Data update script has started running')
    import tiniusconsol
    print('Tinius Data update script has run without error')
except:
    print("Tiniusconsol skipped due to error")

print('Program has run successfully and took '+ str(round((time.time()-tic),2)) + ' seconds to run')