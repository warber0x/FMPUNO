/* @Author: Radouane SAMIR
   @Version: 0.1
   @Chip version: AM29F010 A29040
   
   This code is tested on AM29F010.
   
   For AM29F040B the command sequence are little bit different:
   0x555 rather than 0x5555 see the datasheet. But the timing is the same
   
   You are free to modify the code as you want, but please keep my name as is.
*/

#include <avr/io.h>
#include <util/delay.h>

/* Flash SIZE, used only in read operation*/
#define FLASHSIZE 131072 

uint32_t address = 0;
uint32_t gameSize = 0;

char buffer[20] = {0};
char cmd = 0;
int  index = 0;
char tab[10] = {0};

/* Need a fast change mode IN/OUT */

void flash_change_pins_mode(boolean io)
{
  if (io) {
    DDRD &= ~(1<<2);
    DDRD &= ~(1<<3);
    DDRD &= ~(1<<4);
    DDRD &= ~(1<<5);
    DDRD &= ~(1<<6);
    DDRD &= ~(1<<7);
    DDRB &= ~(1<<0);
    DDRB &= ~(1<<1);
  }
  else
  {
    DDRD |= (1<<2);
    DDRD |= (1<<3);
    DDRD |= (1<<4);
    DDRD |= (1<<5);
    DDRD |= (1<<6);
    DDRD |= (1<<7);
    DDRB |= (1<<0);
    DDRB |= (1<<1);
  }
}

void flash_ctrl_deselect()
{
  digitalWrite(10, HIGH);  //CE
  digitalWrite(12, HIGH);  //WE
  digitalWrite(11, HIGH);  //OE
}

void flash_ctrl_rd()
{
  digitalWrite(11, LOW);
  _delay_us(1);
  digitalWrite(10, LOW);
  _delay_us(1);
}

void flash_ctrl_wr()
{
  digitalWrite(10, LOW);
  _delay_us(1);
  digitalWrite(12, LOW);
  _delay_us(1);
}  

/**************************************************
   Function to access to 
   the highest addresses in the chip 
   Highest 16bits is given to the function
   and do a bit manipulation to set pins High/Low
***************************************************/

void flash_set_highest_addresses(uint16_t addr)
{ 
  /* Highest addresses */
  
  if (addr&bit(0))
  PORTC |= _BV(PORTC2);
  else
  PORTC &= ~_BV(PORTC2);
  
  if (addr&bit(1))
  PORTC |= _BV(PORTC1);
  else
  PORTC &= ~_BV(PORTC1);
  
  if (addr&bit(2))
  PORTC |= _BV(PORTC0);
  else
  PORTC &= ~_BV(PORTC0);
}

/****
 * Shift registers manipulation
 *******************************/

void flash_enable_latch()
{
  /* Shift register Latch */
  digitalWrite(A4, HIGH); 
}

void flash_disable_latch()
{
  /* Shift register Latch */
  digitalWrite(A4, LOW);
}

void flash_enable_serial_clock()
{
  /* Shift register Serial clock */
  digitalWrite(A3, HIGH);
}

void flash_disable_serial_clock()
{
  digitalWrite(A3, LOW);
}

/** 
 * Calculated the given address
 * shift register manipulation
 **************************************/ 

void flash_send_serial_data(uint16_t data)
{ 
  /* Shift register manipulation */
  /* Respect the wiring */
  
  uint16_t addr = 0;
  byte octect1 = 0; 
  byte octect2 = 0;
  
  addr = (data<<8);
  octect1 = (addr>>8);
  
  addr = (data>>8);
  octect2 = addr;
  
  flash_disable_latch();
  for (int i=7;i>=0; i--)
  {
    flash_disable_serial_clock();
    if (octect2&(1<<i))
    PORTC |= _BV(PORTC5);
    else
    PORTC &= ~_BV(PORTC5);
    flash_enable_serial_clock();
  }
  
  
  for (int i=7;i>=0; i--)
  {
    flash_disable_serial_clock();
    if (octect1&(1<<i))
    PORTC |= _BV(PORTC5);
    else
    PORTC &= ~_BV(PORTC5);
    flash_enable_serial_clock();
  }
  flash_enable_latch();
}

/**
 * Set the address *
 *******************/

void flash_addr_set(uint32_t addr)
{
  /* Send address  to the shift register  */
  
  uint16_t LSB;
  uint16_t MSB;
  
  LSB = addr;
  MSB = (addr>>16);
  
  flash_send_serial_data(LSB);
  flash_set_highest_addresses(MSB);
}

/**
 * Calculate the data given and set change pins state
 *****************************************************/

void flash_data_set(uint8_t data)
{
  uint8_t temp;
  uint8_t temp2;
  
  temp = (data<<2);
  temp2 = (data>>6);
  
  for (int i = 2; i < 8; i++)
  {
    if (temp&bit(i))
    {
      DDRD |= (1<<i);
      PORTD |= (1<<i);
    }
    else
    {
      PORTD &= ~(1<<i);
      DDRD &= ~(1<<i);  
    }
   
  }
  
  if(temp2&(1<<0)) 
  {
    DDRB |= _BV(PORTB0);
    PORTB |= _BV(PORTB0);
  }
  else
  {
    PORTB &= ~_BV(PORTB0);
    DDRB &= ~(1<<0);
  }
  
  if(temp2&(1<<1))
  {
    DDRB |= _BV(PORTB1);
    PORTB |= _BV(PORTB1);
  }
  else
  {
    PORTB &= ~_BV(PORTB1);
    DDRB &= ~_BV(PORTB1);
  }
}

/** 
 * Get Data from the chip *
 * MIND: the pull-down resistors
 *********************************/

byte flash_data_get()
{
  /* get data from data bus */
  
  byte data = 0;
  boolean state = LOW;
  boolean state2 = LOW;
  
  for (int i = 2, j = 0; i <= 9; i++, j++)
  {
        state = digitalRead(i);  
        state2 = digitalRead(i); 
        if (state == state2)
           if (state == HIGH)
           bitWrite(data, j, HIGH); 
           
  }
  return data;
}

/*
 * Data polling in programming operation
 *****************************************/

boolean flash_DQ7_byte_poll(uint32_t addr, byte data)
{
  byte octect = 0;
  flash_change_pins_mode(1);
  flash_addr_set(addr);
  flash_ctrl_rd();
  octect = (flash_data_get()>>7);
  while (octect!=(data>>7));
  flash_ctrl_deselect();
  return true;
}

boolean flash_DQ7_erase_poll()
{
  byte octect = 0;
  flash_change_pins_mode(1);
  octect = (flash_data_get()>>7);
  
  while (octect!=1)
  octect = (flash_data_get()>>7);
  
  if (octect)
  Serial.println("Erasure complete");
  
  flash_ctrl_deselect();
  return true;
}

/****
 * Set command sequence and send it to the chip
 ***********************************************/

void flash_send_command(uint32_t addr, uint8_t data)
{
  /* Send command sequence */
  
  flash_addr_set(addr);
  delayMicroseconds(1);
  flash_ctrl_wr();

  flash_data_set(data);
  delayMicroseconds(1);
}

/****
 * Autoselect mode to get info from the chip
 * It's useful to test the chip before any operation
 ******************************************************/

void flash_device_id()
{
  /* This is used to get code identification 
   * from the chip in autoselect mode
   * See the datasheet
   ******************************************/
  
  flash_ctrl_deselect();
  
  //digitalWrite(11, HIGH);
  
  delay(1000);
  
  flash_change_pins_mode(0);
  
  flash_send_command(0x5555, 0xAA);
  flash_ctrl_deselect();
  
  
  flash_send_command(0x2AAA, 0x55);
  flash_ctrl_deselect();
  
  flash_send_command(0x5555, 0x90);
  flash_ctrl_deselect();
 
  delay(1000);
  
  flash_change_pins_mode(1);

  flash_addr_set(0x01);
  delay(1);
  flash_ctrl_rd();
  
  Serial.print(flash_data_get(), HEX);
  //Serial.print("Get device ID complete, Please wait restarting the chip ... ");
  delay(1);
  flash_reset_chip();
  //Serial.println("Done.");
  delay(1000);
  flash_ctrl_deselect();
}

/** AM29F040 **/
/***************/

void flash_get_id_40()
{
  /* This is used to get code identification 
   * from the chip in autoselect mode
   * See the datasheet
   ******************************************/
   
  byte data = 0x00;
  
  flash_ctrl_deselect();
  
  //digitalWrite(11, HIGH);
  
  delay(1000);
  
  flash_change_pins_mode(0);
  
  flash_send_command(0x555, 0xAA);
  flash_ctrl_deselect();
  
  flash_send_command(0x2AA, 0x55);
  flash_ctrl_deselect();
  
  flash_send_command(0x555, 0x90);
  flash_ctrl_deselect();
 
  delay(1000);
  
  flash_change_pins_mode(1);
  
  flash_addr_set(0x00);
  flash_ctrl_rd();
  
  data = flash_data_get();
  
  if (data < 0x0A) 
  Serial.print("0");
  
  Serial.print(data, HEX);
  
  flash_ctrl_deselect();
  
  flash_reset_chip();
  delay(1000);
}


void flash_get_id()
{
  /* This is used to get code identification 
   * from the chip in autoselect mode
   * See the datasheet
   ******************************************/
   
  byte data = 0x00;
  
  flash_ctrl_deselect();
  
  //digitalWrite(11, HIGH);
  
  delay(1000);
  
  flash_change_pins_mode(0);
  
  flash_send_command(0x5555, 0xAA);
  flash_ctrl_deselect();
  
  flash_send_command(0x2AAA, 0x55);
  flash_ctrl_deselect();
  
  flash_send_command(0x5555, 0x90);
  flash_ctrl_deselect();
 
  delay(1000);
  
  flash_change_pins_mode(1);
  
  flash_addr_set(0x00);
  flash_ctrl_rd();
  
  data = flash_data_get();
  
  if (data < 0x0A) 
  Serial.print("0");
  
  Serial.print(data, HEX);
  
  flash_ctrl_deselect();
  
  flash_reset_chip();
  delay(1000);
}

void flash_read_memory(uint32_t addr)
{
  /* Read the chip until the address given */  
  int c = 0;
  
  flash_change_pins_mode(1);
  
  for (uint32_t i = 0; i < addr; i++)
  {
    flash_ctrl_deselect();
    
    flash_addr_set(i);
    
    flash_ctrl_rd();
    
    Serial.print(flash_data_get(),HEX); 
    flash_ctrl_deselect();
  }
}

/* This is the sequence to program a byte on the memory *
 * 0x5555 0x2AAA is for AM29F010
 * 0x555 0x2AA is for AM29F040 A29F040
 ********************************************************/

boolean flash_program_byte(uint32_t addr, uint8_t data)
{
  flash_ctrl_deselect();
  
  flash_send_command(0x5555, 0xAA); 
  flash_ctrl_deselect();
  
  flash_send_command(0x2AAA, 0x55);
  flash_ctrl_deselect();
  
  flash_send_command(0x5555, 0xA0);
  flash_ctrl_deselect();
  
  //Program Address & Program data
  flash_send_command(addr, data);
  flash_ctrl_deselect();
  
  /** Data Polling **/
  while (!flash_DQ7_byte_poll(addr, data));
  
  return true;
}

/* This is the sequence to program a byte on the memory *
 * 0x5555 0x2AAA is for AM29F010
 * 0x555 0x2AA is for AM29F040 A29F040
 ********************************************************/

void flash_reset_chip()
{
  /* This is reset command for the AM29F010 */
  
  flash_ctrl_deselect();
  
  flash_send_command(0x5555, 0xAA);
  flash_ctrl_deselect();
  
  flash_send_command(0x2AAA, 0x55);
  flash_ctrl_deselect();
  
  flash_send_command(0x5555, 0xF0);
  flash_ctrl_deselect();
  
  delay(1000);
}

/* This is the sequence to program a byte on the memory *
 * 0x5555 0x2AAA is for AM29F010
 * 0x555 0x2AA is for AM29F040 A29F040
 ********************************************************/

void flash_erase_memory()
{
  flash_ctrl_deselect();
  delay(1000);
  
  //flash_change_pins_mode(0);
  
  flash_send_command(0x5555, 0xAA);
  flash_ctrl_deselect();
  
  flash_send_command(0x2AAA, 0x55);
  flash_ctrl_deselect();
  
  flash_send_command(0x5555, 0x80);
  flash_ctrl_deselect();
  
  flash_send_command(0x5555, 0xAA);
  flash_ctrl_deselect();
  
  flash_send_command(0x2AAA, 0x55);
  flash_ctrl_deselect();
  
  flash_send_command(0x5555, 0x10);
  flash_ctrl_deselect();
  
  _delay_ms(1000);
  //flash_DQ7_erase_poll();
  flash_reset_chip();
  Serial.print("Erasure Complete");
}

/* To erase AM29F040 */
/*********************/

void flash_erase_memory2()
{
  flash_ctrl_deselect();
  delay(1000);
  
  //flash_change_pins_mode(0);
  
  flash_send_command(0x555, 0xAA);
  flash_ctrl_deselect();
  
  flash_send_command(0x2AA, 0x55);
  flash_ctrl_deselect();
  
  flash_send_command(0x555, 0x80);
  flash_ctrl_deselect();
  
  flash_send_command(0x555, 0xAA);
  flash_ctrl_deselect();
  
  flash_send_command(0x2AA, 0x55);
  flash_ctrl_deselect();
  
  flash_send_command(0x555, 0x10);
  flash_ctrl_deselect();
  
  _delay_ms(1000);
  //flash_DQ7_erase_poll();
  //flash_reset_chip();
  Serial.print("Erasure Complete");
}

/*
 * Read data coming from the computer's USB port *
 *************************************************/

void receiveDataFromPC()
{
  if (Serial.available()>0)
  {
    uint8_t data = Serial.read();
    flash_program_byte(address++, data); 
  }
}

/* Intiate the programing when the python GUI send a trigger */
/*************************************************************/

void startProgramming()
{
    flash_change_pins_mode(0);
    
    Serial.print("+");
    while (!Serial.available());
    while (Serial.available() > 0)
    {
      char car = Serial.read();
      delay(10);
      tab[index++]=car;
      
    }
    tab[index] = '\0';
    
    Serial.print("+");
    
    while(address <= atol(tab)) {
    receiveDataFromPC();
    }
}

void setup()
{
  Serial.begin(115200);
  //ANALOG_CONFIG;
  
  int c = 0;
 
  //Set the shift register pins
  
  pinMode(A5, OUTPUT);
  pinMode(A4, OUTPUT);
  pinMode(A3, OUTPUT);
  
  //set the highest address pins
  
  pinMode(A2, OUTPUT);
  pinMode(A1, OUTPUT);
  pinMode(A0, OUTPUT);
  
  //Set the chip controller
  
  pinMode(10, OUTPUT);
  pinMode(11, OUTPUT);
  pinMode(12, OUTPUT);
  
  //Set data pin mode
  pinMode(2, OUTPUT);
  pinMode(3, OUTPUT);
  pinMode(4, OUTPUT);
  pinMode(5, OUTPUT);
  pinMode(6, OUTPUT);
  pinMode(7, OUTPUT);
  pinMode(8, OUTPUT);
  pinMode(9, OUTPUT);
  
  delay(1000);
  
  address = 0;
  
  flash_ctrl_deselect();
}

void loop()
{ 
  while (!Serial.available());
  cmd = Serial.read();
  
  switch(cmd)
  {
    case 'R':
    flash_read_memory(0xFF);
    Serial.println("");
    break;
    
    case 'E':
    flash_erase_memory();
    Serial.println("");
    break;
    
    case 'W':
    startProgramming();
    Serial.println("");
    break;
    
    case 'I':
    flash_get_id();
    Serial.println("");
    break;
    
    case 'D':
    flash_device_id();
    Serial.println("");
    break;
  
    default:
    cmd = 0;
  }
  cmd = 0;
  index = 0;
  memset(tab, '\0', sizeof(tab));
  delay(10);
}
