# 베이스 이미지 선택 (OpenJDK 사용)
FROM openjdk:17-jdk-alpine


# JAR 파일을 컨테이너 내부로 복사
ARG JAR_FILE=./spring/planner-0.0.1-SNAPSHOT.jar
COPY ${JAR_FILE} app.jar

# 컨테이너가 실행될 때 JAR 파일 실행
ENTRYPOINT ["java", "-jar", "/app.jar"]