/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package hotel.management.system;

import java.awt.*;

import javax.swing.border.EmptyBorder;

import net.proteanit.sql.DbUtils;
import java.sql.*;	
import javax.swing.*;

import java.awt.event.ActionListener;
import java.awt.event.ActionEvent;

public class CustomerInfo extends JFrame {
	Connection conn = null;
	private JPanel contentPane;
	private JLabel lblId;
	private JLabel lblNewLabel;
	private JLabel lblGender;
	private JTable table;
	private JLabel lblCountry;
	private JLabel lblRoom;
	private JLabel lblStatus;
	private JLabel lblNewLabel_1;

	/**
	 * Launch the application.
	 */
	public static void main(String[] args) {
		EventQueue.invokeLater(new Runnable() {
			public void run() {
				try {
					CustomerInfo frame = new CustomerInfo();
					frame.setVisible(true);
				} catch (Exception e) {
					e.printStackTrace();
				}
			}
		});
	}
	public void close()
	{
		this.dispose();
	}
	/**
	 * Create the frame.
	 * @throws SQLException 
	 */
	public CustomerInfo() throws SQLException {
		//conn = Javaconnect.getDBConnection();
		setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		setBounds(300, 150, 920, 600);
		contentPane = new JPanel();
		contentPane.setBorder(new EmptyBorder(5, 5, 5, 5));
		setContentPane(contentPane);
		contentPane.setLayout(null);

		JLabel lblSearchForRoom = new JLabel("Customer Information");
		lblSearchForRoom.setFont(new Font("Tahoma", Font.BOLD, 20));
		lblSearchForRoom.setBounds(310, 8, 250, 31);
		contentPane.add(lblSearchForRoom);
		
		JButton btnExit = new JButton("Back");
		btnExit.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				new Reception().setVisible(true);
                                setVisible(false);
			}
		});
		btnExit.setBounds(450, 510, 120, 30);
        btnExit.setBackground(Color.BLACK);
        btnExit.setForeground(Color.WHITE);
		contentPane.add(btnExit);
		
		JButton btnLoadData = new JButton("Load Data");
		btnLoadData.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent arg0) {
				try{
                                    conn c  = new conn();
                                    
				String displayCustomersql = "select * from Customer";
				ResultSet rs = c.s.executeQuery(displayCustomersql);
				table.setModel(DbUtils.resultSetToTableModel(rs));
			}
				catch(Exception e)
				{
					e.printStackTrace();
				}
			}
				
			
		});
		btnLoadData.setBounds(300, 510, 120, 30);
		btnLoadData.setBackground(Color.BLACK);
		btnLoadData.setForeground(Color.WHITE);
		contentPane.add(btnLoadData);
		
		table = new JTable();
		table.setBounds(0, 100, 900, 380);
		contentPane.add(table);

		lblId = new JLabel("ID");
		lblId.setBounds(31, 50, 46, 14);
		contentPane.add(lblId);
                
        JLabel l1 = new JLabel("ID Number");
		l1.setBounds(110, 50, 80, 14);
		contentPane.add(l1);
		
		lblNewLabel = new JLabel("Mobile No.");
		lblNewLabel.setBounds(210, 50, 65, 14);
		contentPane.add(lblNewLabel);
		
		lblGender = new JLabel("Name");
		lblGender.setBounds(330, 50, 46, 14);
		contentPane.add(lblGender);	
	
		lblCountry = new JLabel("Gender");
		lblCountry.setBounds(420, 50, 46, 14);
		contentPane.add(lblCountry);
		
		lblRoom = new JLabel("Country");
		lblRoom.setBounds(510, 50, 46, 14);
		contentPane.add(lblRoom);

		lblRoom = new JLabel("Room");
		lblRoom.setBounds(610, 50, 46, 14);
		contentPane.add(lblRoom);
		
		lblStatus = new JLabel("Check-in Status");
		lblStatus.setBounds(700, 50, 100, 14);
		contentPane.add(lblStatus);
		
		lblNewLabel_1 = new JLabel("Deposit");
		lblNewLabel_1.setBounds(810, 50, 100, 14);
		contentPane.add(lblNewLabel_1);
                
                getContentPane().setBackground(Color.WHITE);
	}
}