# sale_enhancement

Sale Enhancement Module
This module enhances the Sales Orders in Odoo by adding deadline tracking, priority levels, customer ratings, and automated overdue checks to help teams manage urgent deliveries better.​

Key Features
Tracks delivery deadlines with automatic overdue status updates via daily cron job
Sets priority levels (low, medium, high) with visual tree view colors: green for low, yellow for high, red for overdue
Copies customer ratings (0-5 scale) from partners to orders automatically
Blocks order confirmation without a delivery deadline and validates high-priority deadlines within 3 days of order date​

Setup Steps
Install the saleenhancement module from your addons path
The module extends sale.order and res.partner models automatically
A daily cron job computes overdue statuses; activate it in Settings > Technical > Automation > Scheduled Actions
New "Extra Info" tab appears on sales order forms with all new fields (readonly for computed ones)​

Security & Access
Creates two groups: Sales Manager (full access) and Sales User (read-only for deadline/priority fields)
Assign users to groups via Settings > Users & Companies > Groups​

Usage Tips
Use the server action "Mark Deadline Extended by 3 Days" from sales order form/list views to push deadlines and log activity
Portal customers see priority and overdue filters in their sales order list for self-service tracking
