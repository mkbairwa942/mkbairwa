/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package hotel.management.system;

import java.awt.*;

import java.sql.*;	
import javax.swing.*;
import javax.swing.border.EmptyBorder;

import java.awt.event.ActionListener;
import java.awt.event.ActionEvent;

public class UpdateCheck extends JFrame {
	Connection conn = null;
	PreparedStatement pst = null;
	private JPanel contentPane;
	private JTextField txt_ID;
	private JTextField txt_Room;
	private JTextField txt_Status;
	private JTextField txt_Mobile;
	private JTextField txt_Date;
	private JTextField txt_Time;
	private JTextField txt_Payment;

        Choice c1, c2;
	/**
	 * Launch the application.
	 */
	public static void main(String[] args) {
		EventQueue.invokeLater(new Runnable() {
			public void run() {
				try {
					UpdateCheck frame = new UpdateCheck();
					frame.setVisible(true);
				} catch (Exception e) {
					e.printStackTrace();
				}
			}
		});
	}
	public void close(){
		this.dispose();
	}

	/**
	 * Create the frame.
	 * @throws SQLException 
	 */
	public UpdateCheck() throws SQLException {
		//conn = Javaconnect.getDBConnection();
		setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		setBounds(280, 150, 950, 500);
		contentPane = new JPanel();
		contentPane.setBorder(new EmptyBorder(5, 5, 5, 5));
		setContentPane(contentPane);
		contentPane.setLayout(null);
		
		JLabel lblUpdateCheckStatus = new JLabel("Check-In Details");
		lblUpdateCheckStatus.setFont(new Font("Tahoma", Font.BOLD, 30));
		lblUpdateCheckStatus.setBounds(320, 11, 300, 25);
		contentPane.add(lblUpdateCheckStatus);
                
		// ImageIcon i1  = new ImageIcon(ClassLoader.getSystemResource("icons/nine.jpg"));
		// JLabel l1 = new JLabel(i1);
		// l1.setBounds(425,70,476,290);
		// add(l1);
		
		ImageIcon i1  = new ImageIcon(ClassLoader.getSystemResource("icons/nine.jpg"));
		Image i3 = i1.getImage().getScaledInstance(475, 340,Image.SCALE_DEFAULT);
		ImageIcon i2 = new ImageIcon(i3);
		JLabel l1 = new JLabel(i2);
		l1.setBounds(425,70,475,340);
		add(l1);

		JLabel lblNewLabel = new JLabel("Name :");
		lblNewLabel.setBounds(25, 80, 46, 14);
		contentPane.add(lblNewLabel);
                
                c1 = new Choice();
                try{
                    conn c = new conn();
                    ResultSet rs = c.s.executeQuery("select * from customer");
                    while(rs.next()){
                        c1.add(rs.getString("Namee"));    
                    }
                }catch(Exception e){ }
                c1.setBounds(248, 80, 140, 20);
		contentPane.add(c1);
		
		JLabel lblNewLabel_1 = new JLabel("Room Number :");
		lblNewLabel_1.setBounds(25, 120, 107, 14);
		contentPane.add(lblNewLabel_1);
                
		txt_ID = new JTextField();
		txt_ID.setBounds(248, 120, 140, 20);
		contentPane.add(txt_ID);
		
		JLabel lblNewLabel_2 = new JLabel("Id Number : ");
		lblNewLabel_2.setBounds(25, 160, 97, 14);
		contentPane.add(lblNewLabel_2);

		txt_Status = new JTextField();
		txt_Status.setBounds(248, 160, 140, 20);
		contentPane.add(txt_Status);
		txt_Status.setColumns(10);

		JLabel lblNewLabel_6 = new JLabel("Mobile No : ");
		lblNewLabel_6.setBounds(25, 200, 97, 14);
		contentPane.add(lblNewLabel_6);

		txt_Mobile = new JTextField();
		txt_Mobile.setBounds(248, 200, 140, 20);
		contentPane.add(txt_Mobile);
		txt_Mobile.setColumns(10);
		
		JLabel lblNewLabel_3 = new JLabel("Checked-in :");
		lblNewLabel_3.setBounds(25, 240, 107, 14);
		contentPane.add(lblNewLabel_3);
		
		txt_Date = new JTextField();
		txt_Date.setBounds(248, 240, 140, 20);
		contentPane.add(txt_Date);
		txt_Date.setColumns(10);

		JLabel lblNewLabel_4 = new JLabel("Amount Paid (Rs) : ");
		lblNewLabel_4.setBounds(25, 280, 107, 14);
		contentPane.add(lblNewLabel_4);

		txt_Time = new JTextField();
		txt_Time.setBounds(248, 280, 140, 20);
		contentPane.add(txt_Time);
		txt_Time.setColumns(10);
		
		JLabel lblNewLabel_5 = new JLabel("Pending Amount (Rs) : ");
		lblNewLabel_5.setBounds(25, 320, 150, 14);
		contentPane.add(lblNewLabel_5);

		txt_Payment = new JTextField();
		txt_Payment.setBounds(248, 320, 140, 20);
		contentPane.add(txt_Payment);
		txt_Payment.setColumns(10);
		
		JButton btnUpdate = new JButton("Update");
		btnUpdate.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent ae) { 
                            try{
                                conn c = new conn();
                                
                                String s1 = c1.getSelectedItem();
								String s2 = txt_ID.getText(); //room_number;    
                                String s3 = txt_Status.getText(); //id number  
								String s4 = txt_Mobile.getText(); //mobile
                                String s5 = txt_Date.getText(); //status;    
                                String s6 = txt_Time.getText(); //deposit    
				
                                c.s.executeUpdate("update customer set Room_No = '"+s2+"', ID_Number = '"+s3+"', Mobile = '"+s4+"', Timee = '"+s5+"', Deposit = '"+s6+"' where Namee = '"+s1+"'");
                                
                                JOptionPane.showMessageDialog(null, "Data Updated Successfully");
                                new Reception().setVisible(true);
                                setVisible(false);
                            }catch(Exception ee){
                                System.out.println(ee);
                            }				
				
				
				
			}
		});
		btnUpdate.setBounds(168, 378, 89, 23);
                btnUpdate.setBackground(Color.BLACK);
                btnUpdate.setForeground(Color.WHITE);
		contentPane.add(btnUpdate);
		
		JButton btnExit = new JButton("Back");
		btnExit.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				new Reception().setVisible(true);
                                setVisible(false);
			}
		});
		btnExit.setBounds(281, 378, 89, 23);
                btnExit.setBackground(Color.BLACK);
                btnExit.setForeground(Color.WHITE);
		contentPane.add(btnExit);
		
		JButton btnAdd = new JButton("Check");
		btnAdd.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
                            try{
				String s1 = c1.getSelectedItem();
				conn c = new conn();
								String query1 = "select * from customer where Namee = '"+s1+"'";
								// System.out.println("query is : "+query1);
                                ResultSet rs1 = c.s.executeQuery(query1);
                                
                                while(rs1.next()){
                                    txt_ID.setText(rs1.getString("Room_No"));    
                                    txt_Status.setText(rs1.getString("ID_Number"));    
									txt_Mobile.setText(rs1.getString("Mobile"));
                                    txt_Date.setText(rs1.getString("Timee"));    
                                    txt_Time.setText(rs1.getString("Deposit"));    
                                }
                            }catch(Exception ee){}
                            
                            try{
                                String total = "";
                                conn c  = new conn();
                                ResultSet rs2 = c.s.executeQuery("select * from room where roomnumber = "+txt_ID.getText());
                                while(rs2.next()){
                                    total = rs2.getString("price"); 
                                    
                                }
                                String paid = txt_Time.getText();
                                int pending = Integer.parseInt(total)- Integer.parseInt(paid);
                                
                                txt_Payment.setText(Integer.toString(pending));
                                
                            }catch(Exception ee){}
			}
		});
		btnAdd.setBounds(56, 378, 89, 23);
                btnAdd.setBackground(Color.BLACK);
                btnAdd.setForeground(Color.WHITE);
		contentPane.add(btnAdd);
                
                getContentPane().setBackground(Color.WHITE);
	}

}