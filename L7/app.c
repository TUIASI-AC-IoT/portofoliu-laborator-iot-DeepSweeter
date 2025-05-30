/***************************************************************************//**
 * @file
 * @brief Core application logic.
 *******************************************************************************
 * # License
 * <b>Copyright 2020 Silicon Laboratories Inc. www.silabs.com</b>
 *******************************************************************************
 *
 * SPDX-License-Identifier: Zlib
 *
 * The licensor of this software is Silicon Laboratories Inc.
 *
 * This software is provided 'as-is', without any express or implied
 * warranty. In no event will the authors be held liable for any damages
 * arising from the use of this software.
 *
 * Permission is granted to anyone to use this software for any purpose,
 * including commercial applications, and to alter it and redistribute it
 * freely, subject to the following restrictions:
 *
 * 1. The origin of this software must not be misrepresented; you must not
 *    claim that you wrote the original software. If you use this software
 *    in a product, an acknowledgment in the product documentation would be
 *    appreciated but is not required.
 * 2. Altered source versions must be plainly marked as such, and must not be
 *    misrepresented as being the original software.
 * 3. This notice may not be removed or altered from any source distribution.
 *
 ******************************************************************************/
#include "em_common.h"
#include "app_assert.h"
#include "sl_bluetooth.h"
#include "app.h"
#include "app_log.h"

// The advertising set handle allocated from Bluetooth stack.
static uint8_t advertising_set_handle = 0xff;

/**************************************************************************//**
 * Application Init.
 *****************************************************************************/
SL_WEAK void app_init(void)
{
  /////////////////////////////////////////////////////////////////////////////
  // Put your additional application init code here!                         //
  // This is called once during start-up.                                    //
  /////////////////////////////////////////////////////////////////////////////
}

/**************************************************************************//**
 * Application Process Action.
 *****************************************************************************/
SL_WEAK void app_process_action(void)
{
  /////////////////////////////////////////////////////////////////////////////
  // Put your additional application code here!                              //
  // This is called infinitely.                                              //
  // Do not call blocking functions from here!                               //
  /////////////////////////////////////////////////////////////////////////////
}

/**************************************************************************//**
 * Bluetooth stack event handler.
 * This overrides the dummy weak implementation.
 *
 * @param[in] evt Event coming from the Bluetooth stack.
 *****************************************************************************/
void sl_bt_on_event(sl_bt_msg_t *evt)
{
  sl_status_t sc;
  uint8_t i, tlen, type, len;

  switch (SL_BT_MSG_ID(evt->header)) {
    // -------------------------------
    // This event indicates the device has started and the radio is ready.
    // Do not call any stack command before receiving this boot event!
    case sl_bt_evt_system_boot_id:
      // Create an advertising set.
//      sc = sl_bt_advertiser_create_set(&advertising_set_handle);
//      app_assert_status(sc);
//
//      // Generate data for advertising
//      sc = sl_bt_legacy_advertiser_generate_data(advertising_set_handle,
//                                                 sl_bt_advertiser_general_discoverable);
//      app_assert_status(sc);
//
//      // Set advertising interval to 100ms.
//      sc = sl_bt_advertiser_set_timing(
//        advertising_set_handle,
//        160, // min. adv. interval (milliseconds * 1.6)
//        160, // max. adv. interval (milliseconds * 1.6)
//        0,   // adv. duration
//        0);  // max. num. adv. events
//      app_assert_status(sc);
//      // Start advertising and enable connections.
//      sc = sl_bt_legacy_advertiser_start(advertising_set_handle,
//                                         sl_bt_legacy_advertiser_connectable);
//      app_assert_status(sc);

      sc =  sl_bt_scanner_set_parameters(sl_bt_scanner_scan_mode_passive, 10, 10);
      app_assert_status(sc);

      sc = sl_bt_scanner_start(sl_bt_scanner_scan_phy_1m, sl_bt_scanner_discover_observation);
      app_assert_status(sc);

      break;

    // -------------------------------
    // This event indicates that a new connection was opened.
    case sl_bt_evt_connection_opened_id:
      break;

    // -------------------------------
    // This event indicates that a connection was closed.
    case sl_bt_evt_connection_closed_id:
      // Generate data for advertising
      sc = sl_bt_legacy_advertiser_generate_data(advertising_set_handle,
                                                 sl_bt_advertiser_general_discoverable);
      app_assert_status(sc);

      // Restart advertising after client has disconnected.
      sc = sl_bt_legacy_advertiser_start(advertising_set_handle,
                                         sl_bt_legacy_advertiser_connectable);
      app_assert_status(sc);
      break;

    ///////////////////////////////////////////////////////////////////////////
    // Add additional event handlers here as your application requires!      //
    ///////////////////////////////////////////////////////////////////////////
    case sl_bt_evt_scanner_legacy_advertisement_report_id:
      i = 0;
      tlen = evt->data.evt_scanner_legacy_advertisement_report.data.len;

      while(i<tlen){
          len = evt->data.evt_scanner_legacy_advertisement_report.data.data[i++];
          type = evt->data.evt_scanner_legacy_advertisement_report.data.data[i++];

          if(len == 26 && type == 0xff){
              app_log_hexdump_info(evt->data.evt_scanner_legacy_advertisement_report.data.data[i], 25);

          }
          else{
              i += len-2;
          }
      }
//      for(int i = 0; i < 6; ++i)
//         {
//           app_log_hexdump_reverse_level_s(APP_LOG_LEVEL_INFO, "", evt->data.evt_scanner_legacy_advertisement_report.address.addr, 6);
//         }
         break;
    // -------------------------------
    // Default event handler.
    default:
      break;
  }
}
