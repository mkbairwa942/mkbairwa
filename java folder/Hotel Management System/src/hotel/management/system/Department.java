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
public class Department extends JFrame {
Connection conn = null;
private JPanel contentPane;
private JTable table;
private JLabel lblNewLabel;
private JLabel lblNewLabel_1;

	/**
	 * Launch the application.
	 */
	public static void main(String[] args) {
		EventQueue.invokeLater(new Runnable() {
			public void run() {
				try {
					Department frame = new Department();
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
	public Department() throws SQLException {
		//conn = Javaconnect.getDBConnection();
		setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		setBounds(400, 200, 700, 500);
		contentPane = new JPanel();
		contentPane.setBorder(new EmptyBorder(5, 5, 5, 5));
		setContentPane(contentPane);
		contentPane.setLayout(null);
		
		JLabel lblSearchForRoom = new JLabel("Department Information");
		lblSearchForRoom.setFont(new Font("Tahoma", Font.BOLD, 20));
		lblSearchForRoom.setBounds(220, 10, 250, 31);
		contentPane.add(lblSearchForRoom);

		table = new JTable();
		table.setBounds(0, 80, 700, 250);
		contentPane.add(table);
		
		JButton btnNewButton = new JButton("Load Data");
		btnNewButton.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				try{
                                    conn c = new conn();
                                    
					String displayCustomersql = "select * from Department";
					ResultSet rs = c.s.executeQuery(displayCustomersql);
					table.setModel(DbUtils.resultSetToTableModel(rs));
					
					
				}
				catch (Exception e1){
					e1.printStackTrace();
				}
				
			}
		});
		btnNewButton.setBounds(170, 350, 120, 30);
        btnNewButton.setBackground(Color.BLACK);
        btnNewButton.setForeground(Color.WHITE);
		contentPane.add(btnNewButton);
		
		JButton btnNewButton_1 = new JButton("Back");
		btnNewButton_1.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
					new Reception().setVisible(true);
                                        setVisible(false);
			}
		});
		btnNewButton_1.setBounds(400, 350, 120, 30);
		btnNewButton_1.setBackground(Color.BLACK);
		btnNewButton_1.setForeground(Color.WHITE);
		contentPane.add(btnNewButton_1);
		
		lblNewLabel = new JLabel("Department");
		lblNewLabel.setBounds(145, 50, 105, 14);
		contentPane.add(lblNewLabel);
		
		lblNewLabel_1 = new JLabel("Budget");
		lblNewLabel_1.setBounds(431, 50, 75, 14);
		contentPane.add(lblNewLabel_1);
                
        getContentPane().setBackground(Color.WHITE);
	}

}