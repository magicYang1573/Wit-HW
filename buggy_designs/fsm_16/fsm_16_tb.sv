`timescale 1ns / 100ps
/**********************************************************************
 *
 * File: Test fsm.v   
 *
 **********************************************************************/
//*********************************************************
  module testbench;
//*********************************************************  
     wire  [3:0] state_out;
     reg   clk;
     reg   reset;
     reg   input1, input2;
     fsm_16  DUT(clk, reset, input1, input2, state_out);
  

    `ifdef DUMP_TRACE 
          initial begin
            $dumpfile("dump.vcd");
            $dumpvars(0, DUT);
          end
    `endif // DUMP_TRACE

    integer file;
    initial begin
        string dummy_line;
        file=$fopen("./workload.in","r");
        if(file==0) begin
            $display("Error: could not open file ./workload.in");
            $finish;

        end
        // $fscanf(file,"%s",dummy_line);
        while(!$feof(file))begin
          $fscanf(file,"%b,%b,%b", reset, input1, input2);
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
      $fwrite(f,"time, state_out\n");
      $timeformat(-9,1," ns", 6);
      forever begin
        @(posedge clk);
        $fwrite(f,"%g,%b\n",$time, state_out);
      end

    end

    initial begin
      clk=0;
      forever #5 clk = ~clk;
    end
  
  endmodule