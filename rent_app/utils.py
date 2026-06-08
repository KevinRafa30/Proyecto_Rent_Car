def valida_cedula(p_cedula):
    
    if not p_cedula:
        return False
        
    
    vc_cedula = str(p_cedula).replace("-", "").strip()
    p_long_ced = len(vc_cedula)
    
  
    if p_long_ced != 11 or not vc_cedula.isdigit():
        return False
        
    vn_total = 0
    digito_mult = [1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1]

    for v_dig in range(1, p_long_ced + 1):
        
        index = v_dig - 1
        v_calculo = int(vc_cedula[index]) * digito_mult[index]
        
        if v_calculo < 10:
            vn_total += v_calculo
        else:
            
            v_calculo_str = str(v_calculo)
            vn_total += int(v_calculo_str[0]) + int(v_calculo_str[1])

    return (vn_total % 10 == 0)