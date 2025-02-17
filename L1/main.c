#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <inttypes.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "freertos/queue.h"
#include "driver/gpio.h"

#define GPIO_OUTPUT_IO 4
#define GPIO_OUTPUT_PIN_SEL (1ULL << GPIO_OUTPUT_IO)
#define GPIO_INPUT_IO 2
#define GPIO_INPUT_PIN_SEL (1ULL << GPIO_INPUT_IO)
#define ESP_INTR_FLAG_DEFAULT 0

static QueueHandle_t gpio_evt_queue = NULL;

static void IRAM_ATTR gpio_isr_handler(void* arg)
{
    uint32_t gpio_num = (uint32_t) arg;
    xQueueSendFromISR(gpio_evt_queue, &gpio_num, NULL);
}

void vMyTask()
{
    uint32_t io_num;
    uint32_t ctr = 0;
    for(;;)
    {
        //Task code
        if (xQueueReceive(gpio_evt_queue, &io_num, portMAX_DELAY)) {
            //printf("GPIO[%"PRIu32"] intr, val: %d\n", io_num, gpio_get_level(io_num));
            if(gpio_get_level(io_num) == 1)
                printf("Counter = %ld\n", ctr++);
        }
    }

}


void app_main()
{
    // zero-initialize the config structure.
    gpio_config_t io_conf = {};
    // disable interrupt
    io_conf.intr_type = GPIO_INTR_DISABLE;
    // set as output mode
    io_conf.mode = GPIO_MODE_OUTPUT;
    // bit mask of the pins that you want to set
    io_conf.pin_bit_mask = GPIO_OUTPUT_PIN_SEL;
    // disable pull-down mode
    io_conf.pull_down_en = 0;
    // disable pull-up mode
    io_conf.pull_up_en = 0;
    // configure GPIO with the given settings
    gpio_config(&io_conf);

    io_conf.intr_type = GPIO_INTR_POSEDGE;
    io_conf.pin_bit_mask = GPIO_INPUT_PIN_SEL;
    io_conf.mode = GPIO_MODE_INPUT;
    io_conf.pull_up_en = 1;
    gpio_config(&io_conf);

    //E necesar daca e setata deja intreruperea pe POSEDGE?
    //gpio_set_intr_type(GPIO_INPUT_IO, GPIO_INTR_POSEDGE);

    //create a queue to handle gpio event from isr
    gpio_evt_queue = xQueueCreate(10, sizeof(uint32_t));


    xTaskCreate(vMyTask, "gpio_task_example", 2048, NULL, 10, NULL);

    gpio_install_isr_service(ESP_INTR_FLAG_DEFAULT);
    //hook isr handler for specific gpio pin
    gpio_isr_handler_add(GPIO_INPUT_IO, gpio_isr_handler, (void*) GPIO_INPUT_IO);

    //int cnt = 0;

    while (1)
    {

        //printf("cnt: %d\n", cnt++);
        //BOZO - ADD defines
        gpio_set_level(GPIO_OUTPUT_IO, 0);
        vTaskDelay(1000 / portTICK_PERIOD_MS);
        gpio_set_level(GPIO_OUTPUT_IO, 1);
        vTaskDelay(500 / portTICK_PERIOD_MS);
        gpio_set_level(GPIO_OUTPUT_IO, 0);
        vTaskDelay(250 / portTICK_PERIOD_MS);
        gpio_set_level(GPIO_OUTPUT_IO, 1);
        vTaskDelay(750 / portTICK_PERIOD_MS);

    }
}