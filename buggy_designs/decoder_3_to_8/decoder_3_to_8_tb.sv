`timescale 1ns / 100ps

//*********************************************************
  module testbench;
//*********************************************************  
     wire  Y7, Y6, Y5, Y4, Y3, Y2, Y1, Y0;
     reg   A, B, C;
     reg   en;
     reg   clk;
     // Instantiate the Decoder (named DUT {device under test})
     decoder_3to8  DUT(clk,Y7,Y6,Y5,Y4,Y3,Y2,Y1,Y0, A, B, C, en);
  

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
          $fscanf(file,"%b,%b,%b,%b",A,B,C,en);
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
      $fwrite(f,"time,Y7,Y6,Y5,Y4,Y3,Y2,Y1,Y0\n");
      $timeformat(-9,1," ns", 6);
      forever begin
        @(posedge clk);
        $fwrite(f,"%g,%b,%b,%b,%b,%b,%b,%b,%b\n",$time,Y7,Y6,Y5,Y4,Y3,Y2,Y1,Y0);
      end

    end

    initial begin
      clk=0;
      forever #5 clk = ~clk;
    end
  
  endmodule