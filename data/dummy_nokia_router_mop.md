# Nokia Service Restoration MOP (Method of Procedure)

**Equipment Vendor:** Nokia
**Document Type:** Standard Operating Procedure (SOP)
**Scope:** Core Router Troubleshooting

## Overview
This document outlines the standard procedural steps to identify, troubleshoot, and resolve common network alarms on Nokia Service Routers (SR-Series). Do not skip any mandatory steps.

---

## Procedure to clear ALARM_CODE_404
**Alarm Name:** BGP Peer Down (Authentication Failure)
**Severity:** Critical

This alarm indicates that a BGP peering session has dropped due to an MD5 authentication mismatch.

1. **Verify the Alarm Status:** Run the command `show router bgp neighbor status` to confirm the neighbor is in an Active/Idle state.
2. **Check Logs:** Check the system logs for authentication errors by running `show log log-id 99 | match "auth"`.
3. **Validate Key:** Contact the BGP peer administrator to verify the shared MD5 authentication key.
4. **Update Key:** Enter configure mode `configure router bgp group "EXTERNAL" neighbor 192.168.1.1` and run `authentication-key <NEW_KEY>`.
5. **Clear Session:** Soft reset the BGP session using `clear router bgp protocol`.
6. **Final Verification:** Issue `show router bgp neighbor 192.168.1.1` to confirm the state is now 'Established'.

---

## Procedure to clear ALARM_CODE_501
**Alarm Name:** Interface Link Down (Optical Rx Loss)
**Severity:** Major

This alarm triggers when the optical receiver (Rx) on an SFP module drops below acceptable light levels (-24 dBm).

1. **Check Optical Levels:** Run `show port 1/1/1 optical` to check the current Tx and Rx power levels.
2. **Physical Inspection:** If Rx is below -24 dBm, request remote hands to inspect the fiber patch cord in port 1/1/1 for bends or dirt.
3. **Clean Fiber:** Have the technician clean both ends of the fiber patch cord using an approved optical cleaning pen.
4. **Re-seat SFP:** If cleaning fails, have the technician re-seat (unplug and plug back in) the SFP optic module.
5. **Replace SFP:** If the power levels do not improve, the SFP module is faulty. Replace the SFP module in port 1/1/1 with a new spare.
6. **Verify Link:** Run `show port 1/1/1` to ensure the Operational State is 'Up'.
