`timescale 1ns / 100ps
/**********************************************************************
 *
 * File: Test fsm.v   
 *
 **********************************************************************/
//*********************************************************
  module testbench;
//*********************************************************  
     wire done;
     wire [1162:0] out;
     reg   clk;
     reg   reset;
     reg [192:0] xp, yp, xr, yr;

     // Instantiate the Decoder (named DUT {device under test})
     duursma_lee_algo  DUT(clk, reset, xp, yp, xr, yr, done, out);
  

    `ifdef DUMP_TRACE // used for our OSDD calculations
          initial begin
            $dumpfile("dump.vcd");
            $dumpvars(0, DUT);
          end
    `endif // DUMP_TRACE

    integer file;
    integer cycle_cnt = 0;
    initial begin
        file=$fopen("./workload.in","r");
        if(file==0) begin
            $display("Error: could not open file ./workload.in");
            $finish;

        end
        while(!$feof(file))begin
          $fscanf(file,"%b,%b,%b,%b,%b", reset, xp, yp, xr, yr);
          // $display(reset, xp, yp, xr, yr);
          #10;
          // cycle_cnt = cycle_cnt + 1;
          // if(cycle_cnt%100==0)
          //   $display(cycle_cnt);
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
        $fwrite(f,"%g,%d,%d \n",$time, done, out);
      end

    end

    initial begin
      clk=0;
      forever #5 clk = ~clk;
    end
  
  endmodule