pragma solidity ^0.4.8;
contract MyContract {
    struct rating {
        address userId;
        uint movieId;
        uint rating;
    }
    
    struct final_rating_struct {
        uint movieId;
        uint rating;
    }
    event movie_input (
            address userId,
            uint movieId,
            uint rating
            );
    
    rating[] mv_rating;
    rating[] public mv_rating_origin;
    final_rating_struct[] public final_optimization_score;
    uint total_sum_1;
    uint total_sum_2;
    uint total_mean_1;
    uint total_mean_2;
    uint total_std_1;
    uint total_std_2;
    mapping (uint => mapping (uint => uint)) adjust_score;
    mapping (uint => mapping (uint => uint)) final_score;
    mapping (uint => mapping (uint => uint)) score;
    mapping (uint => uint) public movie_score;
    uint max_temp;
    uint min_temp;
    uint credit_1;
    uint credit_2;
    uint temp_for_credit_1;
    uint temp_for_credit_2;
    uint length_1;
    uint length_2;

    function MyContract() {
        mv_rating.push(rating(0,0,0));
        mv_rating_origin.push(rating(0,0,0));
        final_optimization_score.push(final_rating_struct(0,0));
        for (uint k=1 ; k<mv_rating.length ; k++) {
            for (uint l=1 ; l<=20 ; l++){
                adjust_score[l][0] = 0;
                adjust_score[l][1] = 0;
                adjust_score[l][2] = 0;
                final_score[l][0] = 0;
                final_score[l][1] = 0;
                final_score[l][2] = 0;
            }
        }
    }

    function ScoreCal(uint movie_id, uint movie_rating) {
       
       uint credit_score_1;
       uint credit_score_2;
       uint temp_1;
       uint temp_2;
       
    
    
       mv_rating.push(rating(msg.sender, movie_id, movie_rating));
       mv_rating_origin.push(rating(msg.sender, movie_id, movie_rating));
       movie_input(msg.sender, movie_id, movie_rating);
        
        for (uint i=0 ; i <= mv_rating.length-1 ; i++) {
            if (mv_rating[i].userId == 0x40065078A3c29C6038558740C365cD382974B4AE) {
                credit_score_1 += mv_rating[i].rating;
                temp_1 += 1;
            }
            if (mv_rating[i].userId == 0x425157664ecd498D080cBfC4A730970F7ba177F3) {
                credit_score_2 += mv_rating[i].rating;
                temp_2 += 1;
            }
        }
        if (temp_1 == 0){
            temp_1 = 1 ;
        }
        total_mean_1 = uint(credit_score_1 / temp_1);
        if (temp_2 == 0){
            temp_2 = 1 ;
        }
        total_mean_2 = uint(credit_score_2 / temp_2);
        StdCal(total_mean_1, total_mean_2,temp_1,temp_2,movie_rating);
    }

    function StdCal(uint total_mean_1, uint total_mean_2,uint temp_1,uint temp_2,uint movie_rating){
        uint std_temp_1;
        uint std_temp_2;
    //cal std
        for (uint j=1 ; j < mv_rating.length ; j++) {
            if (mv_rating[j].userId == 0x40065078A3c29C6038558740C365cD382974B4AE) {
                if (total_mean_1 >= mv_rating[j].rating) {
                    std_temp_1 += (total_mean_1 - mv_rating[j].rating) * (total_mean_1 - mv_rating[j].rating);
                }else {
                    std_temp_1 += (mv_rating[j].rating - total_mean_1) * (mv_rating[j].rating - total_mean_1);
                }
            }
            if (mv_rating[j].userId == 0x425157664ecd498D080cBfC4A730970F7ba177F3) {
                if (total_mean_2 >= mv_rating[j].rating) {
                    std_temp_2 += (total_mean_2 - mv_rating[j].rating) * (total_mean_2 - mv_rating[j].rating);
                }else {
                    std_temp_2 += (mv_rating[j].rating - total_mean_2) * (mv_rating[j].rating - total_mean_2);
                }
            }
        }
        total_sum_1 = std_temp_1;
        if (temp_1 == 0){
            temp_1 = 1;
        }
        total_std_1 = sqrt(total_sum_1 / temp_1);
    
        total_sum_2 = std_temp_2;
        if (temp_2 == 0){
            temp_2 = 1;
        }
        total_std_2 = sqrt(total_sum_2 / temp_2);
    //first time normalization
        for (uint k=1 ; k < mv_rating.length ; k++) {
            if (mv_rating[k].userId == 0x40065078A3c29C6038558740C365cD382974B4AE) {
                if (total_mean_1 >= mv_rating[k].rating) {
                    if (total_std_1 == 0){
                        total_std_1 = 1;
                    }
                    mv_rating[k].rating = uint((total_mean_1 - mv_rating[k].rating) / total_std_1);
                }else {
                    if (total_std_1 == 0){
                        total_std_1 = 1;
                    }
                    mv_rating[k].rating = uint((mv_rating[k].rating - total_mean_1) / total_std_1);
                }
            }
            if (mv_rating[k].userId == 0x425157664ecd498D080cBfC4A730970F7ba177F3) {
                if (total_mean_2 >= mv_rating[k].rating) {
                    if (total_std_2 == 0){
                        total_std_2 = 1;
                    }
                    mv_rating[k].rating = uint((total_mean_2 - mv_rating[k].rating) / total_std_2);
                }else {
                    if (total_std_2 == 0){
                        total_std_2 = 1;
                    }
                    mv_rating[k].rating = uint((mv_rating[k].rating - total_mean_2) / total_std_2);
                }
            }
        }
        ScoreCal2(movie_rating);
    }
    
    function ScoreCal2(uint movie_rating){
        uint dis;
        uint max;
        uint min;
    //find MAX and MIN
        min = mv_rating[0].rating;
        max = mv_rating[0].rating;
        for (uint l=1 ; l<mv_rating.length ; l++) {
            if (mv_rating[l].rating > max) {
                max = mv_rating[l].rating;
            }
            if (mv_rating[l].rating < min) {
                min = mv_rating[l].rating;
            }
        }
        max_temp = max;
        min_temp = min;
    
    //adjust score
        for (uint i=1; i<mv_rating.length ; i++) {
            if (max_temp == min_temp) {
                dis = 1;
            }else {
                dis = max_temp - min_temp;
            }
            score[i][0] = (((mv_rating[i].rating - min_temp) / dis) * 5) + 1;
            score[i][1] = mv_rating[i].movieId;
            if (mv_rating[i].userId == 0x40065078A3c29C6038558740C365cD382974B4AE) {
                score[i][3] = 1;
            }
            if (mv_rating[i].userId == 0x425157664ecd498D080cBfC4A730970F7ba177F3) {
                score[i][3] = 2;
            }
        }

//start of movie

        for (uint m=1 ; m<mv_rating.length ; m++) {
            for (uint n=1 ; n<=20 ; n++){
                if (score[m][1] == n){
                    delete adjust_score[n][0];
                    delete adjust_score[n][1];
                    delete adjust_score[n][2];
                    delete adjust_score[n][3];
                    delete adjust_score[n][5];
                }
                
            }
        }
    //movie mean(2), std(4)
    
        for (uint j=1 ; j<mv_rating.length ; j++) {
            for (uint k=1 ; k<=20 ; k++){
                if (score[j][1] == k){
                    adjust_score[k][0] += score[j][0];
                    adjust_score[k][1] += 1;
                    adjust_score[k][2] = adjust_score[k][0] / adjust_score[k][1];
                    if (score[j][0] > adjust_score[k][2]) {
                        adjust_score[k][3] += ((score[j][0] - adjust_score[k][2]) * (score[j][0] - adjust_score[k][2]));
                    } else {
                        adjust_score[k][3] += ((adjust_score[k][2] - score[j][0]) * (adjust_score[k][2] - score[j][0]));
                    }
                }
            }
        }
    //movie_normalization
    
        for (uint a=1 ; a<=20 ; a++) {
            adjust_score[a][4] = sqrt(adjust_score[a][3]);
        }
        
        for (uint p=1 ; p<mv_rating.length ; p++) {
            for (uint q=1 ; q<=20 ; q++) {
                if (score[p][1] == q){
                    if (score[p][0] > adjust_score[q][2]){
                        if (adjust_score[q][4] == 0){
                            adjust_score[q][4] = 1;
                        }
                        score[p][2] = (score[p][0] - adjust_score[q][2]) / adjust_score[q][4];
                    } else {
                        if (adjust_score[q][4] == 0){
                            adjust_score[q][4] = 1;
                        }
                        score[p][2] = (adjust_score[q][2] - score[p][0]) / adjust_score[q][4];
                    }
                }
            }
        }
        ScoreCal3(movie_rating);
    }
        
    
    function ScoreCal3(uint movie_rating){
    //final_credit
    
        delete temp_for_credit_1;
        delete temp_for_credit_2;
        delete length_1;
        delete length_2;
        for (uint r=1 ; r<mv_rating.length ; r++){
            for (uint s=1 ; s<=20 ; s++) {
                if (score[r][1] == s){
                    if (score[r][3] == 1) {
                        if (score[r][2] <= 2*adjust_score[s][4]) {
                            temp_for_credit_1 += 1;
                            length_1 += 1;
                        } else {
                            temp_for_credit_1 += 0;
                            length_1 += 1;
                        }
                    } 
                    if (score[r][3] == 2) {
                        if (score[r][2] <= 2*adjust_score[s][4]) {
                            temp_for_credit_2 += 1;
                            length_2 += 1;
                        } else {
                            temp_for_credit_2 += 0;
                            length_2 += 1;
                        }
                    }
                }
            }
        }
    
        if (length_1 == 0) {
            length_1 = 1;
        }
        credit_1 = temp_for_credit_1 / length_1;
        if (length_2 == 0) {
            length_2 = 1;
        }
        credit_2 = temp_for_credit_2 / length_2;
    
        for (uint a=1 ; a<=20 ; a++) {
            final_score[a][0] = adjust_score[a][2];
            final_score[a][1] = adjust_score[a][1];
        }
    
        for (uint c=mv_rating.length-1 ; c<mv_rating.length ; c++){
            for (uint d=1 ; d<=20 ; d++) {
                if (score[c][1] == d) {
                    delete final_score[d][2];
                    if (msg.sender == 0x40065078A3c29C6038558740C365cD382974B4AE) {
                        final_score[d][2] = (final_score[d][0] * final_score[d][1] + credit_1 * movie_rating) / (final_score[d][1] + 1);
                    }
                    if (msg.sender == 0x425157664ecd498D080cBfC4A730970F7ba177F3) {
                        final_score[d][2] = (final_score[d][0] * final_score[d][1] + credit_2 * movie_rating) / (final_score[d][1] + 1);
                    }
                    movie_score[d] = final_score[d][2];
                }
            }
        }
    }
        
    function getReturnValue(uint index) public constant returns(uint, uint) {
    //        return (final_optimization_score[index].movieId, final_optimization_score[index].rating);
            return (index, movie_score[index]);
        } 
    
    function sqrt(uint input) returns (uint output) {
        uint temp = (input + 1) / 2;
        output = input;
        while (temp < output) {
            output = temp;
            temp = (input / temp + temp) / 2;
        }
    }
}