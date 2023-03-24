# 將各位數的借位，轉成list儲存
def borrow_list(list1, list2):
    
    # 建立處理每一位數時，對應的被減數list
    minuend_int_list = list1.copy()

    # 建立借位list，其中每個元素都是list，每個位數依序分配一個元素
    borrow_int_list=[]

    # 處理借位
    for digit in range(len(list2)):

        # 判斷是否借位
        if minuend_int_list[digit] < list2[digit]:

            # 尋找最近的非零位數
            for i in minuend_int_list[digit+1:]:
                if i != 0:
                    NotZero = minuend_int_list[digit+1:].index(i)
                    break
            
            # 製作該位數對應的小借位list
            minuend_int_list[digit]=10
            for i in range(NotZero):
                minuend_int_list[digit+1+i]=9
            minuend_int_list[digit+1+NotZero]-=1

            # 放入大借位list
            borrow_int_list.append(minuend_int_list[digit:digit+2+NotZero])
        else:
            # 放入大借位list
            borrow_int_list.append([])
        
    borrow_str_list = []
    for i in borrow_int_list:
        borrow_str_list.append(list(map(str, i)))
        
    return borrow_str_list

# 將各位數的進位，轉成list儲存
def carry_list(list1, list2):
    sum_int_list=[]
    carry_int_list=[0]

    if len(list1) < len(list2):
        list1, list2 = list2, list1

    for i in range(len(list2)):
        sum_int_list.append(list1[i]+list2[i]+carry_int_list[i])
        carry_int_list.append({True:1,False:0}[sum_int_list[i]>=10])
        
    for i in range(len(list2),len(list1)):
        sum_int_list.append(list1[i]+carry_int_list[i])
        carry_int_list.append({True:1,False:0}[sum_int_list[i]>=10])

    carry_int_list.append(carry_int_list.pop(0))
    carry_str_list = list(map(str,carry_int_list))

    return carry_str_list