 #include <iostream>
 #include <vector>
 #include <string>
 #include <assert.h>
 using namespace std;
//brancn1
#define IDLE 0
#define ACCELERATING 1
#define AT_MAX 2
#define DECELERATING 3
//wsl
const uint32_t MAX_ACC_STEP = 123456;
const uint32_t ACC_SPEED = 1000;
const uint32_t START_SPEED = 1000;
typedef struct{
    uint8_t dir;
    uint8_t running;
    uint8_t id;
    uint32_t step_move;
    uint32_t step_count;
    uint32_t step_middle;
    uint32_t speed_frac;
    uint32_t speed_accel;
    uint32_t step_frac;
    uint32_t step_speed;
    uint32_t step_spmax;
    uint8_t step_state;
    uint32_t current_pulse;
} MOTOR;
MOTOR motor0;
#define M0_CLOCKWISE 0

void motorDirSet(uint8_t motor_id,uint8_t dir)
 {

 }
 void motorClkSet(uint8_t morot_id, uint8_t level)
 {

 }
void startMotor(uint8_t motor_id,uint8_t dir,int32_t degree,uint32_t step_spmax,uint32_t speed_accel)
{
    volatile MOTOR *pmotor = NULL;
    if(degree<=0)
        return;
    motorDirSet(motor_id,dir);
    switch(motor_id){
        case 0:
            pmotor=&motor0;
            break;   
    }
    pmotor->dir = dir;
    pmotor->running = 1;
    pmotor->step_move = degree;
    pmotor->step_state = ACCELERATING;
    if((step_spmax==0)||(speed_accel==0)){
        pmotor->step_spmax = MAX_ACC_STEP;
        pmotor->speed_accel = ACC_SPEED;
    }
    else{
        pmotor->step_spmax = step_spmax;
        pmotor-> speed_accel = speed_accel;
    }
    pmotor->step_frac = 0;
    pmotor->speed_frac = 0;
    pmotor->step_speed = START_SPEED;
    pmotor->step_count = 0;
}
static void SPTA_IRQHandler(volatile MOTOR *pmotor)
{
    int carry=0;
    pmotor->step_frac += pmotor->step_speed;
    carry = pmotor->step_frac>>17;
    pmotor->step_frac -= carry<<17;
    if(carry!=0){
        assert(carry==1);
        pmotor->step_count += 1;
        cout << motor0.step_count <<","<< motor0.step_speed<<","<< motor0.step_state+64<< endl;
        motorClkSet(0,1);
        if(pmotor->step_count==pmotor->step_move){
                pmotor->step_state = IDLE;
                pmotor->running = 0;
        }
        else if((pmotor->step_move - pmotor->step_count <= pmotor->step_spmax)
            &&(pmotor->step_count >= (pmotor->step_move>>1))){
            pmotor->step_state = DECELERATING;
        }
        else if(pmotor->step_count>=pmotor->step_spmax){
            pmotor->step_state = AT_MAX;
        }
    }

    switch(pmotor->step_state){
        case ACCELERATING:
            pmotor->speed_frac += pmotor->speed_accel;
            carry = pmotor-> speed_frac>>17;
            pmotor->speed_frac -= (carry<<17);
            if(carry!=0){
                pmotor->step_speed += carry;
            }
            break;
        case AT_MAX:
            break;
        case DECELERATING:
            pmotor->speed_frac += pmotor->speed_accel;
            carry = pmotor->speed_frac>>17;
            pmotor->speed_frac -= (carry<<17);
            if(carry&&(pmotor->step_speed>carry)&&(pmotor->step_speed>START_SPEED)){
                pmotor->step_speed -= carry;
            }
            break;
    }
}
 int main()
 {
    startMotor(0,1,300,100,10000);
    while(motor0.running){
        SPTA_IRQHandler(&motor0);
    }
    printf("%c",'\a');
 }
  
