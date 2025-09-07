`timescale 1ns / 100ps

//*********************************************************
  module testbench;
//*********************************************************  
     wire  [7:0] y;
     wire zero, overflow;
     reg   [3:0] opcode;
     reg   [7:0] a,b;
     reg   clk;
     // Instantiate the Decoder (named DUT {device under test})
     alu  DUT(clk, opcode, a, b, y, zero, overflow);
  

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
          $fscanf(file,"%b,%b,%b", opcode, a, b);
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
      $fwrite(f,"time, y, zero, overflow\n");
      $timeformat(-9,1," ns", 6);
      forever begin
        @(posedge clk);
        $fwrite(f,"%g,%b,%b,%b\n",$time, y, zero, overflow);
      end

    end

    initial begin
      clk=0;
      forever #5 clk = ~clk;
    end
  
  endmodule