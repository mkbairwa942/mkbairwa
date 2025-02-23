package hotel.management.system;

import java.awt.*;

import javax.swing.border.EmptyBorder;

import net.proteanit.sql.DbUtils;

import java.sql.*;	
import javax.swing.*;
import java.awt.event.ActionListener;
import java.awt.event.ActionEvent;
public class Employee extends JFrame {
Connection conn = null;
private JPanel contentPane;
private JTable table;
private JLabel lblNewLabel;
private JLabel lblJob;
private JLabel lblName;
private JLabel lblDepartment;

	/**
	 * Launch the application.
	 */
	public static void main(String[] args) {
		EventQueue.invokeLater(new Runnable() {
			public void run() {
				try {
					Employee frame = new Employee();
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
	public Employee() throws SQLException {
		//conn = Javaconnect.getDBConnection();
		setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		setBounds(280, 150, 1000, 600);
		contentPane = new JPanel();
		contentPane.setBorder(new EmptyBorder(5, 5, 5, 5));
		setContentPane(contentPane);
		contentPane.setLayout(null);
		
		JLabel lblSearchForRoom = new JLabel("Employee information");
		lblSearchForRoom.setFont(new Font("Tahoma", Font.BOLD, 20));
		lblSearchForRoom.setBounds(380, 10, 250, 31);
		contentPane.add(lblSearchForRoom);

		table = new JTable();
		table.setBounds(0, 100, 1000, 400);
		contentPane.add(table);
		
		JButton btnLoadData = new JButton("Load Data");
		btnLoadData.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				try{
                                    conn c = new conn();
				String displayCustomersql = "select * from Employee";
				ResultSet rs = c.s.executeQuery(displayCustomersql);
				table.setModel(DbUtils.resultSetToTableModel(rs));
			}
				catch(Exception e1){
					e1.printStackTrace();
				}
			}
			
		});
		btnLoadData.setBounds(350, 500, 120, 30);
		btnLoadData.setBackground(Color.BLACK);
		btnLoadData.setForeground(Color.WHITE);
		contentPane.add(btnLoadData);
		
		JButton btnExit = new JButton("Back");
		btnExit.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				new Reception().setVisible(true);
                                setVisible(false);
			}
		});
		btnExit.setBounds(510, 500, 120, 30);
		btnExit.setBackground(Color.BLACK);
		btnExit.setForeground(Color.WHITE);
		contentPane.add(btnExit);
		
		lblNewLabel = new JLabel("Name");
		lblNewLabel.setBounds(41, 60, 46, 14);
		contentPane.add(lblNewLabel);
		
		lblJob = new JLabel("Age");
		lblJob.setBounds(159, 60, 46, 14);
		contentPane.add(lblJob);
		
		lblName = new JLabel("Gender");
		lblName.setBounds(273, 60, 46, 14);
		contentPane.add(lblName);
		
		lblDepartment = new JLabel("Job");
		lblDepartment.setBounds(416, 60, 86, 14);
		contentPane.add(lblDepartment);
                
        JLabel l1 = new JLabel("Salary");
		l1.setBounds(536, 60, 86, 14);
		contentPane.add(l1);
                
        JLabel l2 = new JLabel("Phone");
		l2.setBounds(656, 60, 86, 14);
		contentPane.add(l2);
                
        JLabel l3 = new JLabel("Gmail");
		l3.setBounds(786, 60, 86, 14);
		contentPane.add(l3);
                
        JLabel l4 = new JLabel("Aadhar");
		l4.setBounds(896, 60, 86, 14);
		contentPane.add(l4);
                
                getContentPane().setBackground(Color.WHITE);
	}
}