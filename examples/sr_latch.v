module sr_latch(output q, output q_n, input s, input r);
    wire or1_out, or2_out;
    
    or o1 (or1_out, r, q_n);
    not n1 (q, or1_out);
    
    or o2 (or2_out, s, q);
    not n2 (q_n, or2_out);
endmodule
