#include "../headers/rotor.h"
#include "../headers/reflector.h"
#include <stdio.h>
#include <omp.h>
#include <string.h>

const char *CT = "UTJXCENIRYOWWSVUYEHCYRPRBJWZNXDJUNVXWXFEWOUODQDZXJTIQKBIUSMIAXEIJFZXXQWJIBXMPCBWBAFHOAXGBPBDKASZLQOYASNAZPPCUTVFISQZHILWGYCJAUQVUGXHVQWWOXMXWEBWXSBQEG"; // first 150
const char *RN[] = {"I", "II", "III", "IV", "V", "VI", "VII", "VIII"};

// Candidate result for leaderboard
typedef struct { 
    double score; 
    int ord[3], 
    ring[3], 
    pos[3]; 
} Result;

// insert into leaderboard, maintains sort order
void insert_to_leaderboard(Result *tops, Result res) {
    for (int i = 0; i < 10; i++) {
        if (res.score > tops[i].score) {
            for (int j = 9; j > i; j--) tops[j] = tops[j - 1];
            tops[i] = res;
            break;
        }
    }
}

// reimplementation of rotate()
// steps through loose rotor structs directly without the Enigma struct to reduce overhead
void step_rotors(Rotor *rl, Rotor *rm, Rotor *rr) {
    if (notch(rm)) { 
        step(rm); 
        step(rl); 
    }
    else if (notch(rr)) step(rm);
    step(rr);
}

// reimplementation of run() without plugboard
int decrypt_char(Rotor *rl, Rotor *rm, Rotor *rr, const Reflector *ref, int c) {
    step_rotors(rl, rm, rr);
    int v = fwd(rr, c);
    v = fwd(rm, v);
    v = fwd(rl, v);
    v = ref->forward_wiring[v];
    v = rev(rl, v);
    v = rev(rm, v);
    return rev(rr, v);
}

void decrypt_sequence(Rotor rl, Rotor rm, Rotor rr, const Reflector *ref, const int *ct, int len, int *out) {
    for (int i = 0; i < len; i++) {
        out[i] = decrypt_char(&rl, &rm, &rr, ref, ct[i]);
    }
}

double ioc(const int *buf, int len) {
    int counts[26] = {0}, sum = 0;
    for (int i = 0; i < len; i++) counts[buf[i]]++;
    for (int i = 0; i < 26; i++) sum += counts[i] * (counts[i] - 1);
    return (double)sum / (len * (len - 1));
}

double evaluate_candidate(Rotor rl, Rotor rm, Rotor rr, const Reflector *ref, const int *ct, int len) {
    int buf[200];
    decrypt_sequence(rl, rm, rr, ref, ct, len, buf);
    return ioc(buf, len);
}

// searches ring setting and starting positions given a rotor order
// ring search only on right as left and middle barely have any impact, as shown on Ostwald & Weierud's paper
void solve_rotor_settings(int i, int j, int k, const Reflector *ref, const int *ct, int len, Result *my_tops) {
    // unstantiate wiring tables once per rotor combination 
    Rotor rl = build(get(RN[i]), 0, 0);
    Rotor rm = build(get(RN[j]), 0, 0);
    Rotor rr = build(get(RN[k]), 0, 0);

    for (int ring = 0; ring < 26; ring++) {
        rr.ring_setting = ring; // set right ring offset
        for (int pl = 0; pl < 26; pl++) {
            for (int pc = 0; pc < 26; pc++) {
                for (int pr = 0; pr < 26; pr++) {
                    // update initial rotor positions 
                    rl.rotor_position = pl;
                    rm.rotor_position = pc;
                    rr.rotor_position = pr;

                    double score = evaluate_candidate(rl, rm, rr, ref, ct, len);
                    // only insert if score exceeds current 10th place
                    if (score > my_tops[9].score) {
                        Result r = {score, {i, j, k}, {0, 0, ring}, {pl, pc, pr}};
                        insert_to_leaderboard(my_tops, r);
                    }
                }
            }
        }
    }
}

int main() {
    int len = strlen(CT);
    int ct[150];
    for (int i = 0; i < len; i++) ct[i] = CT[i] - 'A';

    Result tops[10] = {0};
    Reflector ref = refl_b();

    #pragma omp parallel for collapse(2)
    for (int i = 0; i < 8; i++) {
        for (int j = 0; j < 8; j++) {
            if (i == j) continue;
            for (int k = 0; k < 8; k++) {
                if (i == k || j == k) continue;

                Result my_tops[10] = {0}; // thread-local top 10 buffer
                solve_rotor_settings(i, j, k, &ref, ct, len, my_tops);

                // merge thread-local candidates into global array
                #pragma omp critical
                for (int x = 0; x < 10; x++) insert_to_leaderboard(tops, my_tops[x]);
            }
        }
    }

    for (int i = 0; i < 10; i++) {
        Result r = tops[i];
        printf("(%.6f, ('%s', '%s', '%s'), 'AA%c', '%c%c%c')\n",
            r.score, RN[r.ord[0]], RN[r.ord[1]], RN[r.ord[2]],
            r.ring[2] + 'A',
            r.pos[0] + 'A', r.pos[1] + 'A', r.pos[2] + 'A');
    }
    return 0;
}

// gcc -O3 -std=c17 -fopenmp solve_rotor.c ../rotor.c ../reflector.c -I../headers -o solve_rotor
