-- Copyright 1986-2023 Xilinx, Inc. All Rights Reserved.
-- --------------------------------------------------------------------------------
-- Tool Version: Vivado v.2022.2.2 (lin64) Build 3788238 Tue Feb 21 19:59:23 MST 2023
-- Date        : Fri Mar 15 08:51:10 2024
-- Host        : maia-sdr-devel running 64-bit unknown
-- Command     : write_vhdl -force -mode synth_stub -rename_top decalper_eb_ot_sdeen_pot_pi_dehcac_xnilix -prefix
--               decalper_eb_ot_sdeen_pot_pi_dehcac_xnilix_ system_maia_sdr_0_stub.vhdl
-- Design      : system_maia_sdr_0
-- Purpose     : Stub declaration of top-level module interface
-- Device      : xc7z010clg225-1
-- --------------------------------------------------------------------------------
library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

entity decalper_eb_ot_sdeen_pot_pi_dehcac_xnilix is
  Port ( 
    s_axi_lite_awprot : in STD_LOGIC_VECTOR ( 2 downto 0 );
    s_axi_lite_awvalid : in STD_LOGIC;
    s_axi_lite_awready : out STD_LOGIC;
    s_axi_lite_wdata : in STD_LOGIC_VECTOR ( 31 downto 0 );
    s_axi_lite_wstrb : in STD_LOGIC_VECTOR ( 3 downto 0 );
    s_axi_lite_wvalid : in STD_LOGIC;
    s_axi_lite_wready : out STD_LOGIC;
    s_axi_lite_bresp : out STD_LOGIC_VECTOR ( 1 downto 0 );
    s_axi_lite_bvalid : out STD_LOGIC;
    s_axi_lite_bready : in STD_LOGIC;
    s_axi_lite_araddr : in STD_LOGIC_VECTOR ( 5 downto 0 );
    s_axi_lite_arprot : in STD_LOGIC_VECTOR ( 2 downto 0 );
    s_axi_lite_arvalid : in STD_LOGIC;
    s_axi_lite_arready : out STD_LOGIC;
    s_axi_lite_rdata : out STD_LOGIC_VECTOR ( 31 downto 0 );
    s_axi_lite_rresp : out STD_LOGIC_VECTOR ( 1 downto 0 );
    s_axi_lite_rvalid : out STD_LOGIC;
    s_axi_lite_rready : in STD_LOGIC;
    m_axi_spectrometer_awaddr : out STD_LOGIC_VECTOR ( 31 downto 0 );
    m_axi_spectrometer_awlen : out STD_LOGIC_VECTOR ( 3 downto 0 );
    m_axi_spectrometer_awsize : out STD_LOGIC_VECTOR ( 2 downto 0 );
    m_axi_spectrometer_awburst : out STD_LOGIC_VECTOR ( 1 downto 0 );
    m_axi_spectrometer_awlock : out STD_LOGIC_VECTOR ( 1 downto 0 );
    m_axi_spectrometer_awcache : out STD_LOGIC_VECTOR ( 3 downto 0 );
    m_axi_spectrometer_awprot : out STD_LOGIC_VECTOR ( 2 downto 0 );
    m_axi_spectrometer_awvalid : out STD_LOGIC;
    m_axi_spectrometer_awready : in STD_LOGIC;
    m_axi_spectrometer_wdata : out STD_LOGIC_VECTOR ( 63 downto 0 );
    m_axi_spectrometer_wstrb : out STD_LOGIC_VECTOR ( 7 downto 0 );
    m_axi_spectrometer_wlast : out STD_LOGIC;
    m_axi_spectrometer_wvalid : out STD_LOGIC;
    m_axi_spectrometer_wready : in STD_LOGIC;
    m_axi_spectrometer_bresp : in STD_LOGIC_VECTOR ( 1 downto 0 );
    m_axi_spectrometer_bvalid : in STD_LOGIC;
    m_axi_spectrometer_bready : out STD_LOGIC;
    m_axi_recorder_awaddr : out STD_LOGIC_VECTOR ( 31 downto 0 );
    m_axi_recorder_awlen : out STD_LOGIC_VECTOR ( 3 downto 0 );
    m_axi_recorder_awsize : out STD_LOGIC_VECTOR ( 2 downto 0 );
    m_axi_recorder_awburst : out STD_LOGIC_VECTOR ( 1 downto 0 );
    m_axi_recorder_awlock : out STD_LOGIC_VECTOR ( 1 downto 0 );
    m_axi_recorder_awcache : out STD_LOGIC_VECTOR ( 3 downto 0 );
    m_axi_recorder_awprot : out STD_LOGIC_VECTOR ( 2 downto 0 );
    m_axi_recorder_awvalid : out STD_LOGIC;
    m_axi_recorder_awready : in STD_LOGIC;
    m_axi_recorder_wdata : out STD_LOGIC_VECTOR ( 63 downto 0 );
    m_axi_recorder_wstrb : out STD_LOGIC_VECTOR ( 7 downto 0 );
    m_axi_recorder_wlast : out STD_LOGIC;
    m_axi_recorder_wvalid : out STD_LOGIC;
    m_axi_recorder_wready : in STD_LOGIC;
    m_axi_recorder_bresp : in STD_LOGIC_VECTOR ( 1 downto 0 );
    m_axi_recorder_bvalid : in STD_LOGIC;
    m_axi_recorder_bready : out STD_LOGIC;
    re_in : in STD_LOGIC_VECTOR ( 15 downto 0 );
    im_in : in STD_LOGIC_VECTOR ( 15 downto 0 );
    interrupt_out : out STD_LOGIC;
    s_axi_lite_clk : in STD_LOGIC;
    s_axi_lite_rst : in STD_LOGIC;
    sampling_clk : in STD_LOGIC;
    clk2x_clk : in STD_LOGIC;
    clk3x_clk : in STD_LOGIC;
    clk : in STD_LOGIC;
    rst : out STD_LOGIC;
    s_axi_lite_awaddr : in STD_LOGIC_VECTOR ( 5 downto 0 )
  );

end decalper_eb_ot_sdeen_pot_pi_dehcac_xnilix;

architecture stub of decalper_eb_ot_sdeen_pot_pi_dehcac_xnilix is
attribute syn_black_box : boolean;
attribute black_box_pad_pin : string;
attribute syn_black_box of stub : architecture is true;
attribute black_box_pad_pin of stub : architecture is "s_axi_lite_awprot[2:0],s_axi_lite_awvalid,s_axi_lite_awready,s_axi_lite_wdata[31:0],s_axi_lite_wstrb[3:0],s_axi_lite_wvalid,s_axi_lite_wready,s_axi_lite_bresp[1:0],s_axi_lite_bvalid,s_axi_lite_bready,s_axi_lite_araddr[5:0],s_axi_lite_arprot[2:0],s_axi_lite_arvalid,s_axi_lite_arready,s_axi_lite_rdata[31:0],s_axi_lite_rresp[1:0],s_axi_lite_rvalid,s_axi_lite_rready,m_axi_spectrometer_awaddr[31:0],m_axi_spectrometer_awlen[3:0],m_axi_spectrometer_awsize[2:0],m_axi_spectrometer_awburst[1:0],m_axi_spectrometer_awlock[1:0],m_axi_spectrometer_awcache[3:0],m_axi_spectrometer_awprot[2:0],m_axi_spectrometer_awvalid,m_axi_spectrometer_awready,m_axi_spectrometer_wdata[63:0],m_axi_spectrometer_wstrb[7:0],m_axi_spectrometer_wlast,m_axi_spectrometer_wvalid,m_axi_spectrometer_wready,m_axi_spectrometer_bresp[1:0],m_axi_spectrometer_bvalid,m_axi_spectrometer_bready,m_axi_recorder_awaddr[31:0],m_axi_recorder_awlen[3:0],m_axi_recorder_awsize[2:0],m_axi_recorder_awburst[1:0],m_axi_recorder_awlock[1:0],m_axi_recorder_awcache[3:0],m_axi_recorder_awprot[2:0],m_axi_recorder_awvalid,m_axi_recorder_awready,m_axi_recorder_wdata[63:0],m_axi_recorder_wstrb[7:0],m_axi_recorder_wlast,m_axi_recorder_wvalid,m_axi_recorder_wready,m_axi_recorder_bresp[1:0],m_axi_recorder_bvalid,m_axi_recorder_bready,re_in[15:0],im_in[15:0],interrupt_out,s_axi_lite_clk,s_axi_lite_rst,sampling_clk,clk2x_clk,clk3x_clk,clk,rst,s_axi_lite_awaddr[5:0]";
attribute X_CORE_INFO : string;
attribute X_CORE_INFO of stub : architecture is "top,Vivado 2022.2.2";
begin
end;
