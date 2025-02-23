/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package hotel.management.system;
import java.awt.*;
import java.awt.event.*;
import javax.swing.*;

public class AddRoom extends JFrame implements ActionListener{

    private JPanel contentPane;
    private JTextField PriceField,Room_Number_field;
    private JComboBox comboBox, comboBox_2, comboBox_3;
    JButton Add_Button,Back_Button;
    Choice c1;

    public static void main(String[] args) {
        new AddRoom().setVisible(true);
    }

    public AddRoom() {
    setBounds(280, 200, 1000, 450);
	contentPane = new JPanel();
	setContentPane(contentPane);
	contentPane.setLayout(null);
        
    ImageIcon i1  = new ImageIcon(ClassLoader.getSystemResource("icons/twelve.jpg"));
    Image i3 = i1.getImage().getScaledInstance(500, 300,Image.SCALE_DEFAULT);
    ImageIcon i2 = new ImageIcon(i3);
    JLabel l15 = new JLabel(i2);
    l15.setBounds(420,30,500,350);
    add(l15);
        
    JLabel l10 = new JLabel("Add Rooms");
    l10.setFont(new Font("Tahoma", Font.BOLD, 18));
	l10.setBounds(194, 10, 170, 22);
	contentPane.add(l10);

	JLabel Room_Number = new JLabel("Room Number");
	Room_Number.setForeground(new Color(25, 25, 112));
	Room_Number.setFont(new Font("Tahoma", Font.BOLD, 14));
	Room_Number.setBounds(64, 70, 170, 22);
	contentPane.add(Room_Number);
        
    Room_Number_field = new JTextField();
	Room_Number_field.setBounds(220, 70, 156, 20);
	contentPane.add(Room_Number_field);
        

	JLabel Availability = new JLabel("Availability");
	Availability.setForeground(new Color(25, 25, 112));
	Availability.setFont(new Font("Tahoma", Font.BOLD, 14));
	Availability.setBounds(64, 110, 170, 22);
	contentPane.add(Availability);
        
    comboBox = new JComboBox(new String[] { "Available", "Occupied" });
	comboBox.setBounds(220, 110, 154, 20);
	contentPane.add(comboBox);


	JLabel Cleaning_Status = new JLabel("Cleaning Status");
	Cleaning_Status.setForeground(new Color(25, 25, 112));
	Cleaning_Status.setFont(new Font("Tahoma", Font.BOLD, 14));
	Cleaning_Status.setBounds(64, 150, 170, 22);
	contentPane.add(Cleaning_Status);
        
    comboBox_2 = new JComboBox(new String[] { "Cleaned", "Dirty" });
	comboBox_2.setBounds(220, 150, 154, 20);
	contentPane.add(comboBox_2);

	JLabel Price = new JLabel("Price");
	Price.setForeground(new Color(25, 25, 112));
	Price.setFont(new Font("Tahoma", Font.BOLD, 14));
	Price.setBounds(64, 190, 170, 22);
	contentPane.add(Price);
        
    PriceField = new JTextField();
	PriceField.setBounds(220, 190, 156, 20);
	contentPane.add(PriceField);

    JLabel Bed_Type = new JLabel("Bed Type");
	Bed_Type.setForeground(new Color(25, 25, 112));
	Bed_Type.setFont(new Font("Tahoma", Font.BOLD, 14));
	Bed_Type.setBounds(64, 230, 170, 22);
	contentPane.add(Bed_Type);

    comboBox_3 = new JComboBox(new String[] { "Single Bed", "Double Bed"});
	comboBox_3.setBounds(220, 230, 154, 20);
	contentPane.add(comboBox_3);

	Add_Button = new JButton("Add");
	Add_Button.addActionListener(this);
	Add_Button.setBounds(64, 321, 150, 33);
    Add_Button.setBackground(Color.BLACK);
    Add_Button.setForeground(Color.WHITE);
	contentPane.add(Add_Button);

	Back_Button = new JButton("Back");
	Back_Button.addActionListener(this);
	Back_Button.setBounds(225, 321, 150, 33);
    Back_Button.setBackground(Color.BLACK);
    Back_Button.setForeground(Color.WHITE);
	contentPane.add(Back_Button);

	
    contentPane.setBackground(Color.WHITE);
    
    }
    
    public void actionPerformed(ActionEvent ae){
        try{
            
            if(ae.getSource() == Add_Button){
                try{
                conn c = new conn();
                String room = Room_Number_field.getText();
                String available = (String)comboBox.getSelectedItem();
                String status = (String)comboBox_2.getSelectedItem();
                String price  = PriceField.getText();
                String type = (String)comboBox_3.getSelectedItem();
                String str = "INSERT INTO room values( '"+room+"', '"+available+"', '"+status+"','"+price+"', '"+type+"')";
                if (room.equals("")){JOptionPane.showMessageDialog(null,"Romm Number Should Not Be Empty"); return;}
                if (price.equals("")){JOptionPane.showMessageDialog(null,"Price Should Not Be Empty"); return;}
              
                
		c.s.executeUpdate(str);
		JOptionPane.showMessageDialog(null, "Room Successfully Added");
                // this.setVisible(false);
               
                }catch(Exception ee){
                    System.out.println(ee);
                }
            }
            else if(ae.getSource() == Back_Button){
                this.setVisible(false);
            }
        }catch(Exception eee){
            
        }
    }
}