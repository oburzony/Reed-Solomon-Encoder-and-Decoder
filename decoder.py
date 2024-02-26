from gf16_operations import generating_poly, gf16_poly_divide, add_arr

# Function for Reed-Solomon decoding
def rs_decode(encodedata):
    # Splitting data into 15-element encoded blocks
    block_size = 15
    blocks = [encodedata[i:i+block_size] for i in range(0, len(encodedata), block_size)]

    num_blocks = (len(encodedata) - 1) // block_size + 1
    
    raw_size = 9  # Size of raw data after decoding
    t = 3  # Number of errors expected to be corrected

    raw_blocks = []  # List to store decoded raw blocks
    for block in blocks:
        initial_block_poly = block
        initial_syndrom_poly = gf16_poly_divide(initial_block_poly, generating_poly)
        initial_weight_s = sum(1 for x in initial_syndrom_poly if x != 0)

        # If weight of the initial syndrome is less than or equal to expected errors
        if  initial_weight_s <= t: 
            # Add zeros to the beginning of syndrome polynomial
            initial_syndrom_poly = [0] * 9 + initial_syndrom_poly
            # Correct errors in the block
            initial_block_poly  = [add_arr[initial_block_poly[i]][initial_syndrom_poly[i]] for i in range(0, len(initial_syndrom_poly))]
            raw_data  = initial_block_poly
            
        # If weight of the initial syndrome is greater than expected errors
        if  initial_weight_s > t:
            block_poly = initial_block_poly
            weight_s = initial_weight_s

            k = 0 
            # Iterate until either all errors are corrected or maximum iterations reached
            while k < 9 :       
                # If weight of the syndrome is greater than expected errors
                if  weight_s > t:
                    # Rotate the polynomial to the right by one position
                    roate_right_poly = [block_poly[-1]] + block_poly[:-1]
                    block_poly = roate_right_poly
                    # Recalculate syndrome polynomial
                    syndrom_poly = gf16_poly_divide(block_poly, generating_poly)
                    weight_s = sum(1 for x in syndrom_poly if x != 0)
                    k = k + 1
                
                # If weight of the syndrome is less than or equal to expected errors
                if  weight_s <= t: 
                    # Add zeros to the beginning of syndrome polynomial
                    syndrom_poly = [0] * 9 + syndrom_poly
                    # Correct errors in the block
                    block_poly  = [add_arr[block_poly[i]][syndrom_poly[i]] for i in range(0, len(syndrom_poly))]
                    # Rotate the block back
                    rotate_back = block_poly[k:] + block_poly[:k]
                    raw_data  = rotate_back
                    k = 9
            try:
                raw_data
            except NameError:
                raw_data = [0,0,0,0,0,0,0,0,0]  # If raw_data is not defined, assign a list of zeros
        
        raw_blocks.append(raw_data[:raw_size])  # Append the decoded raw data to the raw_blocks list
        
    final_blocks = []
    for final_block in raw_blocks:
        final_blocks.extend(final_block)

        
    # Return the final blocks
    return final_blocks
