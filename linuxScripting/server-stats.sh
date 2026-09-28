#!/bin/bash

echo "=========================================="
echo "        SERVER PERFORMANCE STATS"
echo "=========================================="

# -----------------------------
# 1. CPU Usage
# -----------------------------
echo ""
echo "CPU Usage:"
echo "------------------------------------------"

CPU_IDLE=$(top -bn1 | grep "Cpu(s)" | awk '{print $8}')
CPU_USAGE=$(awk "BEGIN {print 100 - $CPU_IDLE}")

printf "Total CPU Usage: %.2f%%\n" "$CPU_USAGE"


# -----------------------------
# 2. Memory Usage
# -----------------------------
echo ""
echo "Memory Usage:"
echo "------------------------------------------"

free -h

MEM_TOTAL=$(free | awk '/Mem:/ {print $2}')
MEM_USED=$(free | awk '/Mem:/ {print $3}')
MEM_FREE=$(free | awk '/Mem:/ {print $4}')

MEM_PERCENT=$(awk "BEGIN {printf \"%.2f\", ($MEM_USED/$MEM_TOTAL)*100}")

echo "Total Memory : $(free -h | awk '/Mem:/ {print $2}')"
echo "Used Memory  : $(free -h | awk '/Mem:/ {print $3}')"
echo "Free Memory  : $(free -h | awk '/Mem:/ {print $4}')"
echo "Usage        : $MEM_PERCENT%"


# -----------------------------
# 3. Disk Usage
# -----------------------------
echo ""
echo "Disk Usage:"
echo "------------------------------------------"

df -h /

DISK_TOTAL=$(df -h / | awk 'NR==2 {print $2}')
DISK_USED=$(df -h / | awk 'NR==2 {print $3}')
DISK_FREE=$(df -h / | awk 'NR==2 {print $4}')
DISK_PERCENT=$(df -h / | awk 'NR==2 {print $5}')

echo "Total Disk : $DISK_TOTAL"
echo "Used Disk  : $DISK_USED"
echo "Free Disk  : $DISK_FREE"
echo "Usage      : $DISK_PERCENT"


# -----------------------------
# 4. Top 5 Processes by CPU
# -----------------------------
echo ""
echo "Top 5 Processes by CPU Usage:"
echo "------------------------------------------"

ps -eo pid,ppid,comm,%cpu,%mem --sort=-%cpu | head -n 6


# -----------------------------
# 5. Top 5 Processes by Memory
# -----------------------------
echo ""
echo "Top 5 Processes by Memory Usage:"
echo "------------------------------------------"

ps -eo pid,ppid,comm,%cpu,%mem --sort=-%mem | head -n 6


# -----------------------------
# STRETCH GOALS
# -----------------------------

echo ""
echo "Operating System:"
echo "------------------------------------------"

if [ -f /etc/os-release ]; then
    grep PRETTY_NAME /etc/os-release | cut -d '"' -f 2
fi


echo ""
echo "System Uptime:"
echo "------------------------------------------"

uptime -p


echo ""
echo "Load Average:"
echo "------------------------------------------"

uptime


echo ""
echo "Logged-in Users:"
echo "------------------------------------------"

who


echo ""
echo "=========================================="
echo "          END OF SERVER STATS"
echo "=========================================="