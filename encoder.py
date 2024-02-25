from gf16_operations import generating_poly, gf16_poly_divide

# Encoding function
def rs_encode(data, txt_console):

    # Splitting data into 9-element blocks
    block_size = 9
    num_blocks = (len(data) - 1) // block_size + 1
    blocks = [data[i:i+block_size] for i in range(0, len(data), block_size)]
    
    # Generating error correction blocks 
    ecc_size = 6
    ecc_blocks = []
    for block in blocks:
        block_poly = block
        block_ecc_poly = block_poly + [0] * 6
        block_ecc_poly =  gf16_poly_divide(block_ecc_poly, generating_poly)
        ecc_blocks.append(block_ecc_poly[:ecc_size])

    # Combining data blocks with error correction blocks
    final_blocks = []
    for i in range(num_blocks):
        data_block = blocks[i]
        ecc_block = ecc_blocks[i]
        final_block = data_block + ecc_block
        final_blocks += final_block 
    
    # Returning final blocks
    return final_blocks
