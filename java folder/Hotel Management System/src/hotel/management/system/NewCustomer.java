/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package hotel.management.system;

import java.awt.*;

import javax.swing.border.EmptyBorder;

import java.sql.*;	
import javax.swing.*;
import java.awt.event.ActionListener;
import java.awt.event.ActionEvent;
import java.util.Date;

public class NewCustomer extends JFrame {
	Connection conn = null;
	PreparedStatement pst = null;
	private JPanel contentPane;
	private JTextField ID_Number_Field,Mobile_Number_Field,Customer_Name_Field,Country_Filed,Deposite_Field;
    JComboBox comboBox;
    JRadioButton Malee,Femalee;
    Choice c_room;
    JLabel checkintime,CheckInStatus_Field;

	public static void main(String[] args) {
		EventQueue.invokeLater(new Runnable() {
			public void run() {
				try {
					NewCustomer frame = new NewCustomer();
					frame.setVisible(true);
				} catch (Exception e) {
					e.printStackTrace();
				}
			}
		});
	}

	public NewCustomer() throws SQLException {
		
        setBounds(350, 150, 850, 550);
		contentPane = new JPanel();
		setContentPane(contentPane);
		contentPane.setLayout(null);
                
        ImageIcon i1  = new ImageIcon(ClassLoader.getSystemResource("icons/fifth.png"));
        Image i3 = i1.getImage().getScaledInstance(300, 400,Image.SCALE_DEFAULT);
        ImageIcon i2 = new ImageIcon(i3);
        JLabel l1 = new JLabel(i2);
        l1.setBounds(480,10,300,500);
        add(l1);
		
		JLabel lblNEW_CUSTOMER_FORM = new JLabel("NEW CUSTOMER FORM");
		lblNEW_CUSTOMER_FORM.setFont(new Font("Yu Mincho", Font.PLAIN, 20));
		lblNEW_CUSTOMER_FORM.setBounds(118, 10, 260, 53);
		contentPane.add(lblNEW_CUSTOMER_FORM);
                
        JLabel lblId = new JLabel("ID :");
		lblId.setBounds(35, 70, 200, 14);
		contentPane.add(lblId);
                
        comboBox = new JComboBox(new String[] {"Passport", "Aadhar Card", "Voter Id", "Driving license"});
		comboBox.setBounds(271, 70, 150, 20);
		contentPane.add(comboBox);
                
        JLabel ID_Number = new JLabel("ID Number :");
		ID_Number.setBounds(35, 110, 200, 14);
		contentPane.add(ID_Number);
                
        ID_Number_Field = new JTextField();
		ID_Number_Field.setBounds(271, 110, 150, 20);
		contentPane.add(ID_Number_Field);
		ID_Number_Field.setColumns(10);

        JLabel Lbl_Mobile_Number = new JLabel("Mobile Number :");
		Lbl_Mobile_Number.setBounds(35, 150, 200, 14);
		contentPane.add(Lbl_Mobile_Number);
                
        Mobile_Number_Field = new JTextField();
		Mobile_Number_Field.setBounds(271, 150, 150, 20);
		contentPane.add(Mobile_Number_Field);
		Mobile_Number_Field.setColumns(10);
		
		JLabel lblCustomer_Name = new JLabel("Customer Name :");
		lblCustomer_Name.setBounds(35, 190, 200, 14);
		contentPane.add(lblCustomer_Name);
		
		Customer_Name_Field = new JTextField();
		Customer_Name_Field.setBounds(271, 190, 150, 20);
		contentPane.add(Customer_Name_Field);
		Customer_Name_Field.setColumns(10);

                
		JLabel lblGender = new JLabel("Gender :");
		lblGender.setBounds(35, 230, 200, 14);
		contentPane.add(lblGender);
                
        Malee = new JRadioButton("Male",true);
        Malee.setFont(new Font("Raleway", Font.BOLD, 14));
        Malee.setBackground(Color.WHITE);
        Malee.setBounds(271, 230, 80, 12);
        add(Malee);
                
        Femalee = new JRadioButton("Female");
        Femalee.setFont(new Font("Raleway", Font.BOLD, 14));
        Femalee.setBackground(Color.WHITE);
        Femalee.setBounds(350, 230, 100, 12);
		add(Femalee);

        ButtonGroup bg = new ButtonGroup();
        bg.add(Malee);
        bg.add(Femalee);
                
		JLabel lblCountry = new JLabel("Country :");
		lblCountry.setBounds(35, 270, 200, 14);
		contentPane.add(lblCountry);

        Country_Filed = new JTextField();
		Country_Filed.setBounds(271, 270, 150, 20);
		contentPane.add(Country_Filed);
		Country_Filed.setColumns(10);
		
		JLabel lblReserveRoomNumber = new JLabel("Allocated Room Number :");
		lblReserveRoomNumber.setBounds(35, 310, 200, 14);
		contentPane.add(lblReserveRoomNumber);
                
        c_room = new Choice();
        try{
            conn c = new conn();
            ResultSet rs = c.s.executeQuery("select * from room where availability = 'Available'");
            while(rs.next()){
                c_room.add(rs.getString("roomnumber"));    
            }
        }catch(Exception e){ }
        c_room.setBounds(271, 310, 150, 20);
		contentPane.add(c_room);
		
		JLabel checkintime = new JLabel("Checked-In :"); 
		checkintime.setBounds(35, 350, 200, 14);
		contentPane.add(checkintime);

        Date date = new Date();

        CheckInStatus_Field = new JLabel(""+date);
		CheckInStatus_Field.setBounds(271, 350, 150, 20);
		contentPane.add(CheckInStatus_Field);
		
		JLabel lblDeposite = new JLabel("Deposit :");
		lblDeposite.setBounds(35, 390, 200, 14);
		contentPane.add(lblDeposite);
		
		Deposite_Field = new JTextField();
		Deposite_Field.setBounds(271, 390, 150, 20);
		contentPane.add(Deposite_Field);
		Deposite_Field.setColumns(10);

		JButton AddButton = new JButton("Add");
        AddButton.setBounds(100, 440, 120, 30);
        AddButton.setBackground(Color.BLACK);
        AddButton.setForeground(Color.WHITE);
		contentPane.add(AddButton);
		AddButton.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
                            conn c = new conn();
                            String radio = null;
                            
                            if(Malee.isSelected()){ 
                                radio = "Male";
                            }
                            else if(Femalee.isSelected()){ 
                                radio = "Female";
                            }
                            
                            
                          
                            try{
	    			
                    String ID = (String)comboBox.getSelectedItem(); 
                    String ID_num =  ID_Number_Field.getText();
                    String Mo_No =  Mobile_Number_Field.getText();
	    			String Cus_Nam =  Customer_Name_Field.getText();
                    String Gender =  radio;
	    			String Country =  Country_Filed.getText();
                    String Room = c_room.getSelectedItem();
	    			String CheckInStatu =  CheckInStatus_Field.getText();
                    String Deposit =  Deposite_Field.getText();
                    
                    String q1 = "insert into customer values('"+ID+"','"+ID_num+"','"+Mo_No+"','"+Cus_Nam+"','"+Gender+"','"+Country+"','"+Room+"','"+CheckInStatu+"','"+Deposit+"')";
                    // System.out.println("Sql Query is :"+q1);
                    String q2 = "update room set availability = 'Occupied' where roomnumber = "+Room;
                    // System.out.println("Sql Query is :"+q2);


                    if (ID_num.equals("")){JOptionPane.showMessageDialog(null,"ID Number Should Not Be Empty"); return;}
                    if (Mo_No.equals("")){JOptionPane.showMessageDialog(null,"Mobile Number Should Not Be Empty"); return;}
                    if (Cus_Nam.equals("")){JOptionPane.showMessageDialog(null,"Customer Name Should Not Be Empty"); return;}
                    if (Country.equals("")){JOptionPane.showMessageDialog(null,"Country Should Not Be Empty"); return;}
                    if (CheckInStatu.equals("")){JOptionPane.showMessageDialog(null,"Status Should Not Be Empty"); return;}
	    			if (Deposit.equals("")){JOptionPane.showMessageDialog(null,"Deposit Should Not Be Empty"); return;}
	    			
                    c.s.executeUpdate(q1);
                    c.s.executeUpdate(q2);

	    			JOptionPane.showMessageDialog(null, "Data Inserted Successfully");
                                new Reception().setVisible(true);
                                setVisible(false);
	    		    }catch(SQLException e1){
	    			System.out.println(e1.getMessage());
	    		    }
		    		catch(NumberFormatException s){
		    			JOptionPane.showMessageDialog(null, "Please enter a valid Number");
			}
			}
		});

		
		JButton btnExit = new JButton("Back");
        btnExit.setBounds(260, 440, 120, 30);
        btnExit.setBackground(Color.BLACK);
        btnExit.setForeground(Color.WHITE);
        contentPane.add(btnExit);

		btnExit.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
                            new Reception().setVisible(true);
                            setVisible(false);
			}
		}); 

                
                getContentPane().setBackground(Color.WHITE);
	}
}