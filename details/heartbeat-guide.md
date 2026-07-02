# Heartbeat Guide

## How It Works
When you receive a heartbeat poll, read HEARTBEAT.md and follow it. If nothing needs attention, reply HEARTBEAT_OK. OpenClaw silently discards it.

## Heartbeat vs Cron

**Use heartbeat when:**
- Multiple checks can batch together (inbox + calendar + notifications in one turn)
- You need conversational context from recent messages
- Timing can drift slightly (every ~30 min is fine, not exact)
- You want to reduce API calls by combining periodic checks

**Use cron when:**
- Exact timing matters ("9:00 AM sharp every Monday")
- Task needs isolation from main session history
- You want a different model or thinking level for the task
- One-shot reminders ("remind me in 20 minutes")
- Output should deliver directly to a channel without main session involvement

## Things to Check (if configured)
- **Emails** - Any urgent unread messages?
- **Calendar** - Upcoming events in next 24-48h?
- **Mentions** - Twitter/social notifications?
- **Weather** - Relevant if Warren might go out?

## When to Reach Out
- Important email arrived
- Calendar event coming up (<2h)
- Something interesting found
- It's been >8h since last contact

## When to Stay Quiet
- Late night (23:00-08:00) unless urgent
- Warren is clearly busy
- Nothing new since last check
- Checked <30 minutes ago

## Proactive Work
- Read and organize memory files
- Check on projects (git status, etc.)
- Update documentation
- Review and update MEMORY.md

## Memory Maintenance
Periodically (every few days):
1. Read recent memory/YYYY-MM-DD.md files
2. Distill significant events/lessons into MEMORY.md
3. Remove outdated info from MEMORY.md
Daily files are raw notes; MEMORY.md is curated wisdom.

## Tracking Checks
Optionally track in `memory/heartbeat-state.json`:
```json
{
  "lastChecks": {
    "email": 1703275200,
    "calendar": 1703260800,
    "weather": null
  }
}
```
