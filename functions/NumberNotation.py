

def decimalNotation(Number):
    return ','.join(([str(Number)[:-3][i:i+2] for i in range(0, len(str(Number)[:-3]), 2)]))+','+str(Number)[-3:] if len(str(Number))>3 else str(Number)
