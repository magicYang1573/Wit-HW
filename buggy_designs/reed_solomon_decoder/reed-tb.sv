`timescale 1ns / 100ps
/**********************************************************************
 *
 * File: Test fsm.v   
 *
 **********************************************************************/
//*********************************************************
  module testbench;
//*********************************************************  
    reg clk;
    reg              reset;
    reg              CE;
    reg      [7:0]   input_byte;

    wire  [7:0] Out_byte;
    wire CEO;
    wire Valid_out;

     // Instantiate the Decoder (named DUT {device under test})
    RS_dec  DUT(clk, reset, CE, input_byte, Out_byte, CEO, Valid_out);

    `ifdef DUMP_TRACE
      initial begin
        $dumpfile("dump.vcd");
        $dumpvars(0, DUT);
      end
    `endif

    integer file;
    initial begin
        file=$fopen("./workload.in","r");
        if(file==0) begin
            $display("Error: could not open file ./workload.in");
            $finish;
        end
        while(!$feof(file))begin
          $fscanf(file,"%b,%b,%b", reset, CE, input_byte);
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
      $fwrite(f,"time, Out_byte, CEO, Valid_out\n");
      $timeformat(-9,1," ns", 6);
      forever begin
        @(posedge clk);
        $fwrite(f,"%g,%d,%d,%d \n",$time, Out_byte, CEO, Valid_out);
      end

    end

    initial begin
      clk=0;
      forever #5 clk = ~clk;
    end
  
  endmodule