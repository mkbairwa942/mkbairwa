
import java.awt.*;
import java.awt.event.*;
import java.sql.*;
import javax.swing.*;  

public class Login extends JFrame implements ActionListener{
    
    JLabel l1,l2;
    JTextField t1;
    JPasswordField t2;
    JButton login,cancel;

    Login(){

        super("Login");
        

        setLayout(null);

        l1 = new JLabel("Username");
        l1.setBounds(40,20,100,30);
        add(l1);
        
        l2 = new JLabel("Password");
        l2.setBounds(40,70,100,30);
        add(l2);
 
        t1=new JTextField();
        t1.setBounds(150,20,150,30);
        add(t1);

        t2=new JPasswordField();
        t2.setBounds(150,70,150,30);
        add(t2);
        
        ImageIcon i1 = new ImageIcon(ClassLoader.getSystemResource("icons/second.jpg"));
        Image i2 = i1.getImage().getScaledInstance(200,200,Image.SCALE_DEFAULT);
        ImageIcon i3 =  new ImageIcon(i2);
        JLabel l3 = new JLabel(i3);
        l3.setBounds(350,10,150,150);
        add(l3);
        

        login = new JButton("Login");
        login.setBounds(40,140,120,30);
        login.setFont(new Font("serif",Font.BOLD,15));        
        login.setBackground(Color.BLACK);
        login.setForeground(Color.WHITE);
        login.addActionListener(this);
        add(login);

        cancel=new JButton("Cancel");
        cancel.setBounds(180,140,120,30);
        cancel.setFont(new Font("serif",Font.BOLD,15));
        cancel.setBackground(Color.BLACK);
        cancel.setForeground(Color.WHITE);
        cancel.addActionListener(this);
        add(cancel);

        
        
        
        getContentPane().setBackground(Color.WHITE);

        setVisible(true);
        setBounds(470,250,600,300);

    }

    public void actionPerformed(ActionEvent ae){
        if(ae.getSource()==login){
        try{
            conn c1 = new conn();
            String u = t1.getText();
            String v = t2.getText();
            System.out.println("Username is :"+u);
            System.out.println("Password is :"+v);
            
            String q = "select * from login where username='"+u+"' and password='"+v+"'";
            System.out.println("Sql Query is :"+q);
            
            ResultSet rs = c1.s.executeQuery(q); 
            System.out.println("Sql Query is :"+rs);
            if(rs.next()){ 
                new Dashboard().setVisible(true);
                setVisible(false);
            }else{
                JOptionPane.showMessageDialog(null, "Invalid login");
                setVisible(false);
            }
        }catch(Exception e){
            e.printStackTrace();
        }
        }else if(ae.getSource()==cancel){
            System.exit(0);
        }
    }
    public static void main(String[] arg){
        new Login();
    }
}

//
//import java.awt.EventQueue;
//import java.sql.*;	
//import javax.swing.*;
//import java.awt.event.ActionListener;
//import java.awt.event.ActionEvent;
//import java.awt.Image;
//
//public class Login {
//Connection conn = null;
//ResultSet rs = null;
//PreparedStatement pst = null;
//
//	private JFrame frame;
//	private JTextField txt_username;
//	private JPasswordField txt_password;
//
//	/**
//	 * Launch the application.
//	 */
//	public static void main(String[] args) {
//		EventQueue.invokeLater(new Runnable() {
//			public void run() {
//				try {
//					Login window = new Login();
//					window.frame.setVisible(true);
//				} catch (Exception e) {
//					e.printStackTrace();
//				}
//			}
//		});
//	}
//	
//	/**
//	 * Create the application.
//	 * @throws SQLException 
//	 */
//	public Login() throws SQLException {
//		initialize();
//		//conn = Javaconnect.getDBConnection();
//	}
//	public void close(){
//		this.frame.dispose();
//	}
//
//	/**
//	 * Initialize the contents of the frame.
//	 */
//	private void initialize() {
//		frame = new JFrame();
//		frame.setBounds(100, 100, 683, 445);
//		frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
//		frame.getContentPane().setLayout(null);
//		
//		JLabel lblUsername = new JLabel("Username:");
//		lblUsername.setBounds(357, 114, 67, 27);
//		frame.getContentPane().add(lblUsername);
//		
//		JLabel lblPassword = new JLabel("Password:");
//		lblPassword.setBounds(357, 187, 67, 27);
//		frame.getContentPane().add(lblPassword);
//		
//		txt_username = new JTextField();
//		txt_username.setBounds(419, 117, 86, 20);
//		frame.getContentPane().add(txt_username);
//		txt_username.setColumns(10);
//		
//		JButton btnLogin = new JButton("Login");
//		btnLogin.addActionListener(new ActionListener() {
//			public void actionPerformed(ActionEvent arg0) {
//				String loginsql = "select * from Manager where m_name=? and password=?";
////				try{
////					pst = conn.prepareStatement(loginsql);
////					pst.setString(1, txt_username.getText());
////					pst.setString(2, txt_password.getText());
////					
////					rs = pst.executeQuery();
////					if(rs.next()){
////						JOptionPane.showMessageDialog(null, "Login Successful");
////						Manager manager = new Manager();
////						manager.setVisible(true);
////						close();
////					}
////					else
////					{
////						JOptionPane.showMessageDialog(null, "Username and Password is incorrect");
////					}
////				}
////				catch(Exception e){
////					JOptionPane.showMessageDialog(null, "Username and Password is incorrect");
////				}
//			}
//		});
//		btnLogin.setBounds(400, 275, 89, 23);
//		frame.getContentPane().add(btnLogin);
//		
//		txt_password = new JPasswordField();
//		txt_password.setBounds(418, 190, 87, 20);
//		frame.getContentPane().add(txt_password);
//	}
//}