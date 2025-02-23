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

public class UpdateRoom extends JFrame {
Connection conn = null;
PreparedStatement pst = null;
	private JPanel contentPane;
	private JTextField txt_ID;
	private JTextField txt_Ava;
	private JTextField txt_Status;
	private JTextField txt_Room;
        
        Choice c1;

	/**
	 * Launch the application.
	 */
	public static void main(String[] args) {
		EventQueue.invokeLater(new Runnable() {
			public void run() {
				try {
					UpdateRoom frame = new UpdateRoom();
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
	public UpdateRoom() throws SQLException {
		//conn = Javaconnect.getDBConnection();
		setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		setBounds(270, 180, 1000, 400);
		contentPane = new JPanel();
		contentPane.setBorder(new EmptyBorder(5, 5, 5, 5));
		setContentPane(contentPane);
		contentPane.setLayout(null);
                
		ImageIcon i1  = new ImageIcon(ClassLoader.getSystemResource("icons/seventh.jpg"));
		Image i3 = i1.getImage().getScaledInstance(550, 290,Image.SCALE_DEFAULT);
		ImageIcon i2 = new ImageIcon(i3);
		JLabel l1 = new JLabel(i2);
		l1.setBounds(370,20,550,290);
		add(l1);
		
		JLabel lblUpdateRoomStatus = new JLabel("Update Room Status");
		lblUpdateRoomStatus.setFont(new Font("Tahoma", Font.BOLD, 25));
		lblUpdateRoomStatus.setBounds(40, 11, 350, 34);
		contentPane.add(lblUpdateRoomStatus);
		
		JLabel lblNewLabel = new JLabel("Guest Name:");
		lblNewLabel.setBounds(27, 80, 90, 14);
		contentPane.add(lblNewLabel);
                
                c1 = new Choice();
                try{
                    conn c = new conn();
                    ResultSet rs = c.s.executeQuery("select * from customer");
                    while(rs.next()){
                        c1.add(rs.getString("Namee"));    
                    }
                }catch(Exception e){ }
                c1.setBounds(160, 80, 140, 20);
		contentPane.add(c1);
		
		JLabel lblRoomId = new JLabel("Room Number:");
		lblRoomId.setBounds(27, 130, 100, 14);
		contentPane.add(lblRoomId);
		
		txt_Room = new JTextField();
		txt_Room.setBounds(160, 130, 140, 20);
		contentPane.add(txt_Room);
		txt_Room.setColumns(10);

		JLabel lblAvailability = new JLabel("Availability:");
		lblAvailability.setBounds(27, 180, 90, 14);
		contentPane.add(lblAvailability);
		
		txt_Ava = new JTextField();
		txt_Ava.setBounds(160, 180, 140, 20);
		contentPane.add(txt_Ava);
		txt_Ava.setColumns(10);

		JLabel lblCleanStatus = new JLabel("Clean Status:");
		lblCleanStatus.setBounds(27, 230, 90, 14);
		contentPane.add(lblCleanStatus);

		txt_Status = new JTextField();
		txt_Status.setBounds(160, 230, 140, 20);
		contentPane.add(txt_Status);
		txt_Status.setColumns(10);
                
  
                
                JButton b1 = new JButton("Check");
		b1.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
                            try{
                                String s1 = c1.getSelectedItem();
				conn c = new conn();
								String query1 = "select * from customer where Namee = '"+s1+"'";
								// System.out.println("query is : "+query1);
								ResultSet rs1 = c.s.executeQuery(query1);
                                while(rs1.next()){
                                    txt_Room.setText(rs1.getString("Room_No"));    
                                }
                            }catch(Exception ee){}
                            try{
                                conn c  = new conn();
                                ResultSet rs2 = c.s.executeQuery("select * from room where roomnumber = "+txt_Room.getText());
                                while(rs2.next()){
                                    txt_Ava.setText(rs2.getString("availability")); 
                                    txt_Status.setText(rs2.getString("cleaning_status"));
                                }
                            }catch(Exception ee){}
                        }
		});
		b1.setBounds(30, 290, 80, 23);
                b1.setBackground(Color.BLACK);
                b1.setForeground(Color.WHITE);
		contentPane.add(b1);
		
		JButton btnUpdate = new JButton("Update");
		btnUpdate.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) throws NumberFormatException {
				
				try{
                                    conn c = new conn();
                                    String str = "update room set cleaning_status = '"+txt_Status.getText()+"' where roomnumber = "+txt_Room.getText();
                                    c.s.executeUpdate(str);
                                    JOptionPane.showMessageDialog(null, "Update Sucessful");
                                    
                                    new Reception().setVisible(true);
                                    setVisible(false);
				}catch (Exception ee){
					ee.printStackTrace();
				}
				
			
			}
		});
		btnUpdate.setBounds(120, 290, 80, 23);
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
		btnExit.setBounds(210, 290, 89, 23);
                btnExit.setBackground(Color.BLACK);
                btnExit.setForeground(Color.WHITE);
		contentPane.add(btnExit);
		

		
		getContentPane().setBackground(Color.WHITE);
	}

}