`timescale 1ns / 100ps
/**********************************************************************
 *
 * File: Test fsm.v   
 *
 **********************************************************************/
//*********************************************************
  module testbench;
//*********************************************************  


    reg  [23:0]   wr_addr;
    reg  [15:0]              wr_data;
    reg                      wr_enable;

    reg  [23:0]   rd_addr;
    wire [15:0]              rd_data;
    reg                      rd_enable;
    wire                     rd_ready;

    wire                     busy;
    reg                      rst_n;
    reg                      clk;

    wire [12:0]              addr;
    wire [1:0]               bank_addr;
    wire                     data_oe;
    wire [15:0]              data_out;
    reg  [15:0]              data_in;

    reg                     clock_enable;
    reg                     cs_n;
    reg                     ras_n;
    reg                     cas_n;
    reg                     we_n;
    reg                     data_mask_low;
    reg                     data_mask_high;

     // Instantiate the Decoder (named DUT {device under test})
    sdram_controller sdram_controlleri (
    /* HOST INTERFACE */
    .wr_addr(wr_addr), 
    .wr_data(wr_data),
    .rd_data(rd_data), .rd_ready(rd_ready), .rd_addr(rd_addr),
    .busy(busy), .rd_enable(rd_enable), .wr_enable(wr_enable), .rst_n(rst_n), .clk(clk),

    /* SDRAM SIDE */
    .addr(addr), .bank_addr(bank_addr),
    // tri-state replaced: `data`
    .data_oe(data_oe), .data_out(data_out), .data_in(data_in),
    .clock_enable(clock_enable), .cs_n(cs_n), .ras_n(ras_n), .cas_n(cas_n), .we_n(we_n), 
    .data_mask_low(data_mask_low), .data_mask_high(data_mask_high)
);

    `ifdef DUMP_TRACE // used for our OSDD calculations
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
          $fscanf(file,"%b,%b,%b,%b,%b,%b,%b,%b,%b,%b,%b,%b,%b,%b", 
            wr_addr, wr_data, wr_enable, rd_addr, rd_enable, rst_n, data_in,
            clock_enable, cs_n, ras_n, cas_n, we_n, data_mask_low, data_mask_high);
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
      $fwrite(f,"time, rd_data, rd_ready, busy, addr, bank_addr, data_oe, data_out\n");
      $timeformat(-9,1," ns", 6);
      forever begin
        @(posedge clk);
        $fwrite(f,"%g,%d,%d,%d,%d,%d,%d,%d \n",$time, rd_data, rd_ready, busy, addr, bank_addr, data_oe, data_out);
      end

    end

    initial begin
      clk=0;
      forever #5 clk = ~clk;
    end
  
  endmodule