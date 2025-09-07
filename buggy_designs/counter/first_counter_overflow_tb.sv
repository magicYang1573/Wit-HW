`timescale 1ns / 100ps
/**********************************************************************
 *
 * File: Test first_counter_overflow.v   
 *
 **********************************************************************/
//*********************************************************
  module testbench;
//*********************************************************  
     wire  [3:0] counter_out;
     wire overflow_out;
     reg   clk;
     reg   reset, enable;
     // Instantiate the Decoder (named DUT {device under test})
     first_counter  DUT(clk, reset, enable, counter_out, overflow_out);
  

    `ifdef DUMP_TRACE // used for our OSDD calculations
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
          $fscanf(file,"%d,%d", reset, enable);
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
      $fwrite(f,"time, counter_out, overflow_out\n");
      $timeformat(-9,1," ns", 6);
      forever begin
        @(posedge clk);
        $fwrite(f,"%g,%b,%b\n",$time, counter_out, overflow_out);
      end

    end

    initial begin
      clk=0;
      forever #5 clk = ~clk;
    end
  
  endmodule