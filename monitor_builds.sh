#!/bin/bash

# GitHub Actions Build Monitor Script
# Quick monitoring of GitHub Actions workflows

REPO_OWNER="shihan84"
REPO_NAME="hunger-rest"
REPO_URL="https://github.com/${REPO_OWNER}/${REPO_NAME}"

echo "🔄 GitHub Actions Build Monitor"
echo "Repository: ${REPO_URL}"
echo "=================================="

# Function to check workflow status
check_workflows() {
    echo "📊 Checking workflow status..."
    
    # Get workflow runs using GitHub API
    WORKFLOWS=$(curl -s "https://api.github.com/repos/${REPO_OWNER}/${REPO_NAME}/actions/runs?per_page=10" | jq -r '.workflow_runs[] | "\(.status) \(.conclusion // "N/A") \(.name) #\(.run_number) \(.created_at)"')
    
    if [ -z "$WORKFLOWS" ]; then
        echo "❌ No workflow runs found or API error"
        return 1
    fi
    
    echo ""
    echo "Recent Workflow Runs:"
    echo "===================="
    
    while IFS= read -r line; do
        if [ -n "$line" ]; then
            STATUS=$(echo "$line" | awk '{print $1}')
            CONCLUSION=$(echo "$line" | awk '{print $2}')
            NAME=$(echo "$line" | awk '{print $3}')
            RUN_NUM=$(echo "$line" | awk '{print $4}')
            CREATED=$(echo "$line" | awk '{print $5}')
            
            # Status emojis
            case "$STATUS" in
                "completed")
                    if [ "$CONCLUSION" = "success" ]; then
                        EMOJI="✅"
                    else
                        EMOJI="❌"
                    fi
                    ;;
                "in_progress")
                    EMOJI="🔄"
                    ;;
                "queued")
                    EMOJI="⏳"
                    ;;
                *)
                    EMOJI="❓"
                    ;;
            esac
            
            echo "${EMOJI} ${NAME} #${RUN_NUM} - ${STATUS} (${CONCLUSION})"
            echo "   Created: ${CREATED}"
            echo "   URL: https://github.com/${REPO_OWNER}/${REPO_NAME}/actions/runs/${RUN_NUM}"
            echo ""
        fi
    done <<< "$WORKFLOWS"
}

# Function to open GitHub Actions page
open_actions() {
    echo "🌐 Opening GitHub Actions page..."
    if command -v open >/dev/null 2>&1; then
        open "${REPO_URL}/actions"
    elif command -v xdg-open >/dev/null 2>&1; then
        xdg-open "${REPO_URL}/actions"
    else
        echo "Please open: ${REPO_URL}/actions"
    fi
}

# Function to monitor live
monitor_live() {
    INTERVAL=${1:-30}
    echo "🔄 Starting live monitoring (checking every ${INTERVAL} seconds)"
    echo "Press Ctrl+C to stop"
    
    while true; do
        clear
        echo "🔄 GitHub Actions Live Monitor - $(date)"
        echo "=========================================="
        check_workflows
        echo ""
        echo "⏳ Waiting ${INTERVAL} seconds... (Press Ctrl+C to stop)"
        sleep $INTERVAL
    done
}

# Main script logic
case "${1:-status}" in
    "status"|"")
        check_workflows
        ;;
    "open")
        open_actions
        ;;
    "live")
        monitor_live "${2:-30}"
        ;;
    "help")
        echo "Usage: $0 [command]"
        echo ""
        echo "Commands:"
        echo "  status (default) - Show recent workflow runs"
        echo "  open           - Open GitHub Actions page in browser"
        echo "  live [seconds] - Monitor workflows in real-time"
        echo "  help           - Show this help"
        echo ""
        echo "Examples:"
        echo "  $0                    # Show status"
        echo "  $0 open               # Open in browser"
        echo "  $0 live 60           # Monitor every 60 seconds"
        ;;
    *)
        echo "❌ Unknown command: $1"
        echo "Use '$0 help' for usage information"
        exit 1
        ;;
esac
