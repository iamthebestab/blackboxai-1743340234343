import math

def calculate_pieces(L_s, B_s, L_p, B_p):
    """
    Calculate the number of pieces and waste for a given sheet size.
    """
    # Calculate number of pieces in original orientation
    N1 = (L_s // L_p) * (B_s // B_p)
    W1 = (L_s * B_s) - (N1 * L_p * B_p)

    # Calculate number of pieces in rotated orientation
    N2 = (L_s // B_p) * (B_s // L_p)
    W2 = (L_s * B_s) - (N2 * B_p * L_p)

    return (N1, W1) if (N1 > N2 or (N1 == N2 and W1 < W2)) else (N2, W2)

def select_best_sheet(sheets, L_p, B_p):
    """
    Select the best sheet size from a list of options to minimize waste and maximize pieces.
    """
    best_sheet, max_pieces, min_waste = None, 0, float('inf')
    
    for L_s, B_s in sheets:
        pieces, waste = calculate_pieces(L_s, B_s, L_p, B_p)
        if pieces > max_pieces or (pieces == max_pieces and waste < min_waste):
            best_sheet, max_pieces, min_waste = (L_s, B_s), pieces, waste
    
    return best_sheet, max_pieces, min_waste

def calculate_costs(quantity, pieces_per_sheet, sheet_size, gsm, paper_price, pasting_option, no_of_plates,
                    cost_of_printing, cost_of_lamination, cost_of_cutting, cost_of_uv, cost_of_dye, cost_of_leaf):
    """
    Calculate production costs based on material and processing details.
    """
    length_sheet, breadth_sheet = sheet_size
    sheets_needed = math.ceil(quantity / pieces_per_sheet)
    gms = (((length_sheet * breadth_sheet * gsm) / 3100) / 500) * 100
    amount_per_sheet = (gms * paper_price) / 100
    cost_of_paper = amount_per_sheet * sheets_needed
    pasting = cost_of_paper if pasting_option.upper() == 'Y' else 0
    cost_after_pasting = cost_of_paper + pasting
    cost_of_plates = no_of_plates * 250
    cost_of_designing = 1000

    total_cost = (cost_after_pasting + cost_of_plates + cost_of_printing + cost_of_lamination +
                  cost_of_cutting + cost_of_uv + cost_of_dye + cost_of_leaf + cost_of_designing)
    cost_per_piece = total_cost / quantity

    return {
        'Sheets Needed': sheets_needed,
        'Gms': gms,
        'Amount per Sheet': amount_per_sheet,
        'Total Paper Cost': cost_of_paper,
        'Pasting Cost': pasting,
        'Total Cost after Pasting': cost_after_pasting,
        'Plate Cost': cost_of_plates,
        'Total Production Cost': total_cost,
        'Cost per Piece': cost_per_piece
    }