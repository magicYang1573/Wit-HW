`timescale 1ns / 100ps
/**********************************************************************
 *
 * File: Test fsm.v   
 *
 **********************************************************************/
//*********************************************************
  module testbench;
//*********************************************************  
    reg              clk, reset;
    reg      [31:0]  in;
    reg              in_ready, is_last;
    reg      [1:0]   byte_num;

    wire             buffer_full; /* to "user" module */
    wire     [511:0] out;
    wire         out_ready;

     // Instantiate the Decoder (named DUT {device under test})
    keccak  DUT(clk, reset, in, in_ready, is_last, byte_num, buffer_full, out, out_ready);

    
    `ifdef DUMP_TRACE 
          initial begin
            $dumpfile("dump.vcd");
            $dumpvars(0, DUT);
          end
    `endif // DUMP_TRACE
          
    integer file;
    initial begin
        file=$fopen("./workload.in","r");
        if(file==0) begin
            $display("Error: could not open file ./workload.in");
            $finish;
        end
        while(!$feof(file))begin
          $fscanf(file,"%b,%b,%b,%b,%b", reset, in, in_ready, byte_num, is_last);
          // $display("%b,%b,%b,%b,%b,%b,%b,%b,%b", wb_rst_i, arst_i, wb_adr_i, wb_dat_i, wb_we_i, 
          // wb_stb_i, wb_cyc_i, scl_pad_i, sda_pad_i);
          #10;
        end
        $fclose(file);
        $finish;
    end
    
    
    initial begin
      integer f;
      f=$fopen("./output-signals.txt");
      if(f==0) begin
        $display("Error: could not open file ./output-signals.txt");
        $finish;
      end
      $fwrite(f,"time, buffer_full, out, out_ready\n");
      $timeformat(-9,1," ns", 6);
      forever begin
        @(posedge clk);
        $fwrite(f,"%g,%d,%d,%d \n",$time, buffer_full, out, out_ready);
      end

    end

    initial begin
      clk=0;
      forever #5 clk = ~clk;
    end
  
  endmodule