`timescale 1ns / 100ps
/**********************************************************************
 *
 * File: Test led_controller.v   
 *
 **********************************************************************/
//*********************************************************
  module testbench;
//*********************************************************  
     wire  [2:0] lights;
     reg   clk;
     reg   reset, pedestrian_button, car_sensor;
     led_controller  DUT(clk, reset, pedestrian_button, car_sensor, lights);
  

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
          $fscanf(file,"%b,%b,%b", reset, pedestrian_button, car_sensor);
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
      $fwrite(f,"time, lights\n");
      $timeformat(-9,1," ns", 6);
      forever begin
        @(posedge clk);
        $fwrite(f,"%g,%b\n",$time, lights);
      end

    end

    initial begin
      clk=0;
      forever #5 clk = ~clk;
    end
  
  endmodule