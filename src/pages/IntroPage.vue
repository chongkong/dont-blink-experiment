<template>
<v-flex class="intro-page" md6 offset-md3>
  <h1>새로운 실험 참여자는<br>언제나 환영합니다!</h1>
  
  <v-flex md10 offset-md1>
    <v-card>
      <v-card-text>
        <v-form v-model="valid" ref="form" dark>
          <span class="title">참가자 정보</span>
          <v-text-field label="이름 (또는 가명)" v-model="participant.name" :rules="nameRules" required></v-text-field>
          <v-text-field label="나이" v-model="participant.age" :rules="ageRules" required></v-text-field>
          <v-radio-group label="성별" v-model="participant.gender" required row>
            <v-radio label="밝히지 않음" value="U">Prefer not to claim</v-radio>
            <v-radio label="여성" value="F">Female</v-radio>
            <v-radio label="남성" value="M">Male</v-radio>
          </v-radio-group>
          <v-text-field label="소속 학과" 
              v-model="participant.department"
              :rules="departmentRules" required>
          </v-text-field>
          <v-text-field label="연락처" :rules="contactRules" v-model="participant.contact"></v-text-field>
        </v-form>
      </v-card-text>
      <v-card-actions>
        <v-btn flat @click="register">실험 참가하기</v-btn>
      </v-card-actions>
    </v-card>
  </v-flex>
</v-flex>
</template>

<script>
export default {
  data() {
    return {
      valid: false,
      genders: ["U", "F", "M"],
      nameRules: [
        (v) => !!v || "이름을 입력해주세요",
        (v) => v.length <= 10 || "이름이 너무 깁니다"
      ],
      ageRules: [
        (v) => !!v || "나이를 입력해주세요",
        (v) => !!v.match(/[0-9]+/) || "숫자로 입력해주세요"
      ],
      departmentRules: [
        (v) => !!v || "소속 학과를 입력해주세요 (없을 시 '없음')",
        (v) => v.length <= 20 || "소속학과명이 너무 깁니다"
      ],
      contactRules: [
        (v) => !!v || "연락처를 입력해주세요"
      ],
      participant: {
        name: "",
        age: "",
        gender: "U",
        department: "",
        contact: ""
      }
    }
  },
  methods: {
    register() {
      if (this.$refs.form.validate()) {
        this.$store.dispatch("register", this.participant);
      }
    }
  }
}
</script>

<style lang="scss">
.intro-page {
  h1 {
    margin-bottom: 30px;
    text-align: center;
  }
}
</style>
