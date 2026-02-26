// Structural SR Latch using basic OR/NOT gates
module sr_latch(output q, output q_n, input s, input r);
    wire or1_out, or2_out;
    
    or o1 (or1_out, r, q_n);
    not n1 (q, or1_out);
    
    or o2 (or2_out, s, q);
    not n2 (q_n, or2_out);
endmodule

// Behavioral D-FlipFlop for simulation and Waveform generation
module dff(output logic q, input logic d, input logic clk);
    always_ff @(posedge clk) begin
        q <= d;
    end
endmodule

module testbench;
    logic clk, d, s, r;
    logic q_beh, q_str, q_n_str;
    
    sr_latch latch (.q(q_str), .q_n(q_n_str), .s(s), .r(r));
    dff d1 (.q(q_beh), .d(d), .clk(clk));

    initial begin
        $dumpfile("dff_sim.vcd");
        $dumpvars(0, testbench);
        
        // Init signals
        clk = 0; d = 0; s = 0; r = 1; 
        
        #10;
        r = 0; // Latch holds 0
        d = 1;
        
        #10;
        clk = 1; // posedge clk, q_beh=1
        s = 1;   // Latch set to 1
        
        #10;
        clk = 0;
        s = 0;   // Latch holds 1
        d = 0;
        
        #10;
        clk = 1; // posedge clk, q_beh=0
        r = 1;   // Latch resets to 0
        
        #10;
        clk = 0;
        
        #20;
        $finish;
    end
endmodule
