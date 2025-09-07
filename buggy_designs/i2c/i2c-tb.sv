`timescale 1ns / 100ps
/**********************************************************************
 *
 * File: Test fsm.v   
 *
 **********************************************************************/
//*********************************************************
  module testbench;
//*********************************************************  
    reg        clk;     // master clock input
    reg        wb_rst_i;     // synchronous active high reset
    reg        arst_i;       // asynchronous reset
    reg  [2:0] wb_adr_i;     // lower address bits
    reg  [7:0] wb_dat_i;     // databus input
    wire [7:0] wb_dat_o;     // databus output
    reg        wb_we_i;      // write enable input
    reg        wb_stb_i;     // stobe/core select signal
    reg        wb_cyc_i;     // valid bus cycle input
    wire       wb_ack_o;     // bus cycle acknowledge output
    wire       wb_inta_o;    // interrupt request signal output
  
    // I2C signals
    // i2c clock line
    reg  scl_pad_i;       // SCL-line input
    wire scl_pad_o;       // SCL-line output (always 1'b0)
    wire scl_padoen_o;    // SCL-line output enable (active low)
  
    // i2c data line
    reg  sda_pad_i;       // SDA-line input
    wire sda_pad_o;       // SDA-line output (always 1'b0)
    wire sda_padoen_o;    // SDA-line output enable (active low)
  

     // Instantiate the Decoder (named DUT {device under test})
    i2c_master_top  DUT(clk, wb_rst_i, arst_i, wb_adr_i, wb_dat_i, wb_dat_o,
      wb_we_i, wb_stb_i, wb_cyc_i, wb_ack_o, wb_inta_o,
      scl_pad_i, scl_pad_o, scl_padoen_o, sda_pad_i, sda_pad_o, sda_padoen_o);

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
          $fscanf(file,"%b,%b,%b,%b,%b,%b,%b,%b,%b", wb_rst_i, arst_i, wb_adr_i, wb_dat_i, wb_we_i, 
            wb_stb_i, wb_cyc_i, scl_pad_i, sda_pad_i);
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
      $fwrite(f,"time, wb_dat_o, wb_ack_o, wb_inta_o, scl_pad_o, scl_padoen_o, sda_pad_o, sda_padoen_o\n");
      $timeformat(-9,1," ns", 6);
      forever begin
        @(posedge clk);
        $fwrite(f,"%g,%d,%d,%d,%d,%d,%d,%d \n",$time, wb_dat_o, wb_ack_o, wb_inta_o, scl_pad_o, scl_padoen_o, sda_pad_o, sda_padoen_o);
      end

    end

    initial begin
      clk=0;
      forever #5 clk = ~clk;
    end
  
  endmodule