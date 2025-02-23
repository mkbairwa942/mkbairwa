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
import java.util.Date;
import java.awt.event.*;
import java.text.DateFormat;
import javax.swing.text.DateFormatter;

public class CheckOut extends JFrame{
	Connection conn = null;
	PreparedStatement pst = null;
	private JPanel contentPane;
	private JTextField t1,t2,t4;
	JLabel t3;
        Choice c1;

	/**
	 * Launch the application.
	 */
	public static void main(String[] args) {
		EventQueue.invokeLater(new Runnable() {
			public void run() {
				try {
					CheckOut frame = new CheckOut();
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
	public CheckOut() throws SQLException {
		//conn = Javaconnect.getDBConnection();
		setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		setBounds(350, 250, 800, 400);
		contentPane = new JPanel();
		contentPane.setBorder(new EmptyBorder(5, 5, 5, 5));
		setContentPane(contentPane);
		contentPane.setLayout(null);
                
		ImageIcon i1  = new ImageIcon(ClassLoader.getSystemResource("icons/sixth.jpg"));
		Image i3 = i1.getImage().getScaledInstance(370, 300,Image.SCALE_DEFAULT);
		ImageIcon i2 = new ImageIcon(i3);
		JLabel l1 = new JLabel(i2);
		l1.setBounds(370,20,370,300);
		add(l1);
		
		JLabel lblCheckOut = new JLabel("Check Out ");
		lblCheckOut.setFont(new Font("Tahoma", Font.BOLD, 20));
		lblCheckOut.setBounds(120, 10, 140, 35);
		contentPane.add(lblCheckOut);
		
		JLabel lblName = new JLabel("Number :");
		lblName.setBounds(20, 80, 80, 14);
		contentPane.add(lblName);
                
                c1 = new Choice();
                try{
                    conn c = new conn();
                    ResultSet rs = c.s.executeQuery("select * from customer");
                    while(rs.next()){
                        c1.add(rs.getString("Namee"));    
                    }
                }catch(Exception e){ }
                c1.setBounds(130, 80, 180, 20);
		contentPane.add(c1);
                
		JLabel lblRoomNumber = new JLabel("Room Number:");
		lblRoomNumber.setBounds(20, 120, 86, 20);
		contentPane.add(lblRoomNumber);
		
		t1 = new JTextField();
    	t1.setBounds(130, 120, 180, 20);
		contentPane.add(t1);

		JLabel lblCheckIn = new JLabel("Check In Time:");
		lblCheckIn.setBounds(20, 160, 86, 20);
		contentPane.add(lblCheckIn);
		
		t2 = new JTextField();
    	t2.setBounds(130, 160, 180, 20);
		contentPane.add(t2);

		JLabel lblCheckOutt = new JLabel("Check Out Time:");
		lblCheckOutt.setBounds(20, 200, 86, 20);
		contentPane.add(lblCheckOutt);
		
		Date date = new Date();

		t3 = new JLabel(""+date);
    	t3.setBounds(130, 200, 180, 20);
		contentPane.add(t3);

		JLabel lblTotaltime = new JLabel("Total Time:");
		lblTotaltime.setBounds(20, 240, 86, 20);
		contentPane.add(lblTotaltime);
		
		t4 = new JTextField();
    	t4.setBounds(130, 240, 180, 20);
		contentPane.add(t4);

		ImageIcon i4 = new ImageIcon(ClassLoader.getSystemResource("icons/tick.png"));
		Image i5 = i4.getImage().getScaledInstance(20, 20,Image.SCALE_DEFAULT);
		ImageIcon i6 = new ImageIcon(i5);
		
		JButton l2 = new JButton(i6);
		l2.setBounds(320,80,20,20);
		add(l2);
                
                l2.addActionListener(new ActionListener(){
                    
                    public void actionPerformed(ActionEvent ae){
                        System.out.println("Hi");
                        try{
                            
                            conn c = new conn();
                            String namee = c1.getSelectedItem();
                            // ResultSet rs = c.s.executeQuery("select * from customer where Namee = '"+namee+"'");
							String query1 = "select * from customer where Namee = '"+namee+"'";
							System.out.println("query is : "+query1);
							ResultSet rs = c.s.executeQuery(query1);
                            if(rs.next()){
                                System.out.println("clicked");
                                t1.setText(rs.getString("Room_No"));
								t2.setText(rs.getString("Timee"));
								String inTime = t2.getText();
                                // int total = Math.abs(date - DateFormat.(t2));
                                
                                // t4.setText(Integer.toString(total));
 
                            }
                        }catch(Exception e){ }
                    }
                });


		JButton btnCheckOut = new JButton("Check Out");
		btnCheckOut.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
                                String namee = c1.getSelectedItem();
                                String s1 = t1.getText();
				String deleteSQL = "Delete from customer where Namee = '"+namee+"'";
                String q2 = "update room set availability = 'Available' where roomnumber = "+s1;
                 
				conn c = new conn();

	    		try{
	    			c.s.executeUpdate(deleteSQL);
	    			c.s.executeUpdate(q2);
	    			JOptionPane.showMessageDialog(null, "Check Out Successful");
	    			new Reception().setVisible(true);
                                setVisible(false);
	    		}catch(SQLException e1){
	    			System.out.println(e1.getMessage());
	    		}
			}
		});
		btnCheckOut.setBounds(50, 300, 100, 25);
		btnCheckOut.setBackground(Color.BLACK);
		btnCheckOut.setForeground(Color.WHITE);
		contentPane.add(btnCheckOut);
		
		JButton btnExit = new JButton("Back");
		btnExit.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				new Reception().setVisible(true);
                                setVisible(false);
			}
		});
		btnExit.setBounds(160, 300, 100, 25);
		btnExit.setBackground(Color.BLACK);
		btnExit.setForeground(Color.WHITE);
		contentPane.add(btnExit);
                getContentPane().setBackground(Color.WHITE);
	}

}