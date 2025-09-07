`timescale 1ns / 100ps
/**********************************************************************
 *
 * File: Test arbiter.v   
 *
 **********************************************************************/
//*********************************************************
  module testbench;
//*********************************************************  
     wire  [3:0] GRANT_O;
     reg   clk;
     reg   REQUEST1, REQUEST2, REQUEST3, REQUEST4;
     arbiter  DUT(clk, REQUEST1, REQUEST2, REQUEST3, REQUEST4, GRANT_O);
  

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
          $fscanf(file,"%b,%b,%b,%b", REQUEST1, REQUEST2, REQUEST3, REQUEST4);
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
      $fwrite(f,"time, GRANT_O\n");
      $timeformat(-9,1," ns", 6);
      forever begin
        @(posedge clk);
        $fwrite(f,"%g,%b\n",$time, GRANT_O);
      end

    end

    initial begin
      clk=0;
      forever #5 clk = ~clk;
    end
  
  endmodule