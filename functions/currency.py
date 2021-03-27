import decimal    

def num2words(num):
    num = decimal.Decimal(num)
    decimal_part = num - int(num)
    num = int(num)

    under_20 = ['Zero', 'One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Eleven', 'Twelve', 'Thirteen', 'Fourteen', 'Fifteen', 'Sixteen', 'Seventeen', 'Eighteen', 'Nineteen']
    tens = ['Twenty', 'Thirty', 'Forty', 'Fifty', 'Sixty', 'Seventy', 'Eighty', 'Ninety']
    above_100 = {100: 'Hundred', 1000: 'Thousand', 100000: 'Lakhs', 10000000: 'Crores'}

    if num < 20:
        return under_20[num]

    if num < 100:
        return tens[num // 10 - 2] + (' ' if num % 10 == 0 else ' ' + under_20[num % 10])

    # find the appropriate pivot - 'Million' in 3,603,550, or 'Thousand' in 603,550
    pivot = max([key for key in above_100.keys() if key <= num])

    return num2words(num // pivot) + ' ' + above_100[pivot] + (' ' if num % pivot==0 else ' ' + num2words(num % pivot))


def currency(value):
    numlist = str(value).split('.')
    Paise = 'only' 
    Rupees = 'Rupees '+ num2words(int(numlist[0]))+ ' '
    Rupee = ''
    for enumm, value in enumerate(Rupees.split(' ')):
        if enumm!=len(Rupees.split(' ')):
            if value == 'Hundred':
                value = value+' and'
        Rupee = Rupee+' '+value
    
    if len(numlist)>1:
        PaiseAmount=int(numlist[1][:2])
        if len(numlist[1][:2])<2:
            PaiseAmount = int(numlist[1][:2]+'0')
        Paise = 'and '+ num2words(PaiseAmount)+ ' Paise only'

    
    return Rupee.strip()+' '+ Paise
