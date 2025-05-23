#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <string.h>

#ifdef _WIN32
#define CLEAR "cls"
#else
#define CLEAR "clear"
#endif

#define SIZE 5
#define NUM_CANDY 5

typedef struct {
    int size;
    char symbol;
    int found; // 0: 미발견, 1: 발견
    int positions[5][2]; // 최대 5칸 좌표
} Candy;

void clear_screen() {
    system(CLEAR);
}

void init_grid(char grid[SIZE][SIZE]) {
    for(int i=0; i<SIZE; i++)
        for(int j=0; j<SIZE; j++)
            grid[i][j] = '.';
}

void print_grid(char grid[SIZE][SIZE]) {
    printf("   1 2 3 4 5\n");
    for(int i=0; i<SIZE; i++) {
        printf("%d  ", i+1);
        for(int j=0; j<SIZE; j++) {
            printf("%c ", grid[i][j]);
        }
        printf("\n");
    }
}

int valid_position(char grid[SIZE][SIZE], int row, int col, int size, int dir) {
    // dir: 0=가로, 1=세로, 2=오른쪽아래, 3=왼쪽아래, 4=오른쪽위, 5=왼쪽위
    int i;
    if(dir == 0) { // 가로
        if(col + size > SIZE) return 0;
        for(i=0; i<size; i++) if(grid[row][col+i] != '.') return 0;
    } else if(dir == 1) { // 세로
        if(row + size > SIZE) return 0;
        for(i=0; i<size; i++) if(grid[row+i][col] != '.') return 0;
    } else if(dir == 2) { // 오른쪽아래
        if(row + size > SIZE || col + size > SIZE) return 0;
        for(i=0; i<size; i++) if(grid[row+i][col+i] != '.') return 0;
    } else if(dir == 3) { // 왼쪽아래
        if(row + size > SIZE || col - size + 1 < 0) return 0;
        for(i=0; i<size; i++) if(grid[row+i][col-i] != '.') return 0;
    } else if(dir == 4) { // 오른쪽위
        if(row - size + 1 < 0 || col + size > SIZE) return 0;
        for(i=0; i<size; i++) if(grid[row-i][col+i] != '.') return 0;
    } else if(dir == 5) { // 왼쪽위
        if(row - size + 1 < 0 || col - size + 1 < 0) return 0;
        for(i=0; i<size; i++) if(grid[row-i][col-i] != '.') return 0;
    } else {
        return 0;
    }
    return 1;
}

void place_candy(char grid[SIZE][SIZE], Candy* candy) {
    int placed = 0;
    int try_count = 0;
    while(!placed && try_count < 1000) {
        int dir = rand() % 6;
        int row = rand() % SIZE;
        int col = rand() % SIZE;
        if(valid_position(grid, row, col, candy->size, dir)) {
            for(int i=0; i<candy->size; i++) {
                int r=row, c=col;
                if(dir==0) c+=i;
                else if(dir==1) r+=i;
                else if(dir==2) { r+=i; c+=i; }
                else if(dir==3) { r+=i; c-=i; }
                else if(dir==4) { r-=i; c+=i; }
                else if(dir==5) { r-=i; c-=i; }
                grid[r][c] = candy->symbol;
                candy->positions[i][0] = r;
                candy->positions[i][1] = c;
            }
            placed = 1;
        }
        try_count++;
    }
}

void reveal_candy(char grid[SIZE][SIZE], Candy* candy) {
    for(int i=0; i<candy->size; i++) {
        int r = candy->positions[i][0];
        int c = candy->positions[i][1];
        grid[r][c] = candy->symbol;
    }
    candy->found = 1;
}

int is_candy_found(Candy* candy, int row, int col) {
    for(int i=0; i<candy->size; i++)
        if(candy->positions[i][0]==row && candy->positions[i][1]==col)
            return 1;
    return 0;
}

int main() {
    int n = 10; // ★ 삽질 횟수, 필요시 수정
    char ground[SIZE][SIZE];
    char display[SIZE][SIZE];
    Candy candies[NUM_CANDY] = {
        {5, '=', 0, {{0}}},
        {4, '=', 0, {{0}}},
        {3, '=', 0, {{0}}},
        {2, '=', 0, {{0}}},
        {1, '=', 0, {{0}}}
    };

    srand((unsigned int)time(NULL));
    init_grid(ground);
    init_grid(display);

    // 사탕 랜덤 배치
    for(int i=0; i<NUM_CANDY; i++)
        place_candy(ground, &candies[i]);

    // 게임 스토리
    clear_screen();
    printf("막대 사탕 발굴작전!\n");
    printf("크리스마스에 선물받은 막대사탕들을 그린치가 모두 훔쳐가버렸다.\n");
    printf("그린치를 쫓아가보니 그린치가 땅을 파놓은 흔적만을 발견할 수 있었다.\n");
    printf("지금 나에겐 n번 땅을 파내면 부러질 것 같은 10년된 삽 뿐이다.\n");
    printf("나는 꼭 선물받은 막대사탕들을 찾아 돌아갈 것이다.\n\n");
    printf("삽질 기회: %d번\n", n);
    printf("아무 키나 누르면 시작!\n");
    getchar();

    int digs = 0, found_candy = 0;
    while(digs < n) {
        clear_screen();
        printf("남은 삽질 기회: %d\n", n-digs);
        print_grid(display);

        int col, row;
        printf("땅을 팔 위치를 입력하세요 (열 행, 1~5): ");
        scanf("%d %d", &col, &row);
        col -= 1; row -= 1;
        if(row < 0 || row >= SIZE || col < 0 || col >= SIZE) {
            printf("잘못된 좌표입니다. 엔터를 누르세요.\n");
            getchar(); getchar();
            continue;
        }
        if(display[row][col] != '.') {
            printf("이미 판 곳입니다. 엔터를 누르세요.\n");
            getchar(); getchar();
            continue;
        }
        digs++;

        int found = 0;
        for(int i=0; i<NUM_CANDY; i++) {
            if(!candies[i].found && is_candy_found(&candies[i], row, col)) {
                printf("막대사탕 발견!\n");
                reveal_candy(display, &candies[i]);
                found_candy++;
                found = 1;
                break;
            }
        }
        if(!found) {
            display[row][col] = 'x';
            printf("아무것도 발견하지 못했다...\n");
        }
        printf("엔터를 누르면 계속.\n");
        getchar(); getchar();
    }

    clear_screen();
    printf("게임 종료!\n");
    printf("총 %d개의 막대사탕을 찾았습니다!\n", found_candy);
    printf("\n최종 지도:\n");
    print_grid(display);

    // 정답지도(디버깅용)
    // printf("\n정답 지도(디버깅용):\n");
    // print_grid(ground);

    return 0;
}