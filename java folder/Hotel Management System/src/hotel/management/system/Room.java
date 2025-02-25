/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package hotel.management.system;

import java.awt.*;

import javax.swing.border.EmptyBorder;

import net.proteanit.sql.*;

import java.sql.*;	
import javax.swing.*;
import java.awt.event.ActionListener;
import java.awt.event.ActionEvent;
public class Room extends JFrame {
Connection conn = null;
private JPanel contentPane;
private JTable table;
private JLabel lblAvailability;
private JLabel lblCleanStatus;
private JLabel lblNewLabel;
private JLabel lblNewLabel_1;
private JLabel lblRoomNumber;
private JLabel lblId;

	/**
	 * Launch the application.
	 */
	public static void main(String[] args) {
		EventQueue.invokeLater(new Runnable() {
			public void run() {
				try {
					Room frame = new Room();
					frame.setVisible(true);
				} catch (Exception e) {
					e.printStackTrace();
				}
			}
		});
	}

        
	public Room() throws SQLException {
		//conn = Javaconnect.getDBConnection();
		setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		setBounds(220, 130, 1100, 600);
		contentPane = new JPanel();
		contentPane.setBorder(new EmptyBorder(5, 5, 5, 5));
		setContentPane(contentPane);
		contentPane.setLayout(null);
                
		ImageIcon i1  = new ImageIcon(ClassLoader.getSystemResource("icons/eight.jpg"));
		Image i3 = i1.getImage().getScaledInstance(600, 600,Image.SCALE_DEFAULT);
		ImageIcon i2 = new ImageIcon(i3);
		JLabel l1 = new JLabel(i2);
		l1.setBounds(500,0,600,600);
		add(l1);
                
		JLabel lblSearchForRoom = new JLabel("Room Information");
		lblSearchForRoom.setFont(new Font("Tahoma", Font.BOLD, 20));
		lblSearchForRoom.setBounds(170, 11, 186, 31);
		contentPane.add(lblSearchForRoom);

		table = new JTable();
		table.setBounds(0, 80, 500, 350);
		contentPane.add(table);
		
		JButton btnLoadData = new JButton("Load Data");
		btnLoadData.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				try{
                    conn c = new conn();
					String displayCustomersql = "select * from room";
					//PreparedStatement pst = conn.prepareStatement(displayCustomersql);
					ResultSet rs = c.s.executeQuery(displayCustomersql);
					table.setModel(DbUtils.resultSetToTableModel(rs));
					
					
				}
				catch(Exception e1){
					e1.printStackTrace();
				}
			}
		});
		btnLoadData.setBounds(100, 450, 120, 30);
        btnLoadData.setBackground(Color.BLACK);
        btnLoadData.setForeground(Color.WHITE);
		contentPane.add(btnLoadData);
		
		JButton btnNewButton = new JButton("Back");
		btnNewButton.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				new Reception().setVisible(true);
                                setVisible(false);
			}
		});
		btnNewButton.setBounds(290, 450, 120, 30);
		btnNewButton.setBackground(Color.BLACK);
		btnNewButton.setForeground(Color.WHITE);
		contentPane.add(btnNewButton);
		
		lblId = new JLabel("Room Number");
		lblId.setBounds(12, 50, 90, 14);
		contentPane.add(lblId);

		lblAvailability = new JLabel("Availability");
		lblAvailability.setBounds(119, 50, 69, 14);
		contentPane.add(lblAvailability);
		
		lblCleanStatus = new JLabel("Clean Status");
		lblCleanStatus.setBounds(216, 50, 76, 14);
		contentPane.add(lblCleanStatus);
		
		lblNewLabel = new JLabel("Price");
		lblNewLabel.setBounds(330, 50, 46, 14);
		contentPane.add(lblNewLabel);
		
		lblNewLabel_1 = new JLabel("Bed Type");
		lblNewLabel_1.setBounds(417, 50, 76, 14);
		contentPane.add(lblNewLabel_1);

		
	
                
                getContentPane().setBackground(Color.WHITE);
	}

}