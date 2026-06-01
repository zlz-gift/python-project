<script setup>
</script>

<template>
  <footer class="app-footer">
    <div class="footer-content">
      <div class="footer-section">
        <h3>电商系统</h3>
        <p>精选好货，优质生活</p>
        <p>致力于为您提供最优质的购物体验</p>
      </div>
      <div class="footer-section">
        <h4>购物指南</h4>
        <ul>
          <li><a href="#">购物流程</a></li>
          <li><a href="#">支付方式</a></li>
          <li><a href="#">配送说明</a></li>
          <li><a href="#">售后服务</a></li>
        </ul>
      </div>
      <div class="footer-section">
        <h4>服务保障</h4>
        <ul>
          <li><a href="#">正品保证</a></li>
          <li><a href="#">7天退换</a></li>
          <li><a href="#">隐私保护</a></li>
          <li><a href="#">投诉建议</a></li>
        </ul>
      </div>
      <div class="footer-section">
        <h4>联系我们</h4>
        <ul>
          <li>客服热线：400-888-8888</li>
          <li>服务时间：9:00 - 21:00</li>
          <li>邮箱：service@shop.com</li>
          <li>地址：北京市朝阳区</li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <p>&copy; 2024 电商系统 版权所有 | 京ICP备xxxxxxxx号</p>
    </div>
  </footer>
</template>

<style scoped>
.app-footer {
  background: #2c3e50;
  color: #ecf0f1;
  margin-top: 60px;
}

.footer-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 48px 20px 32px;
  display: grid;
  grid-template-columns: 2fr 1fr 1fr 1fr;
  gap: 40px;
}

.footer-section h3 {
  font-size: 22px;
  font-weight: 700;
  margin: 0 0 12px;
  color: white;
}

.footer-section h4 {
  font-size: 16px;
  font-weight: 600;
  margin: 0 0 12px;
  color: white;
}

.footer-section p {
  font-size: 14px;
  color: #bdc3c7;
  margin: 4px 0;
  line-height: 1.6;
}

.footer-section ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.footer-section li {
  font-size: 13px;
  color: #bdc3c7;
  padding: 4px 0;
  line-height: 1.6;
}

.footer-section a {
  color: #bdc3c7;
  text-decoration: none;
  transition: color 0.2s;
}

.footer-section a:hover {
  color: #667eea;
}

.footer-bottom {
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  padding: 20px;
  text-align: center;
}

.footer-bottom p {
  font-size: 13px;
  color: #95a5a6;
  margin: 0;
}

@media (max-width: 768px) {
  .footer-content {
    grid-template-columns: 1fr 1fr;
    gap: 24px;
  }
}

@media (max-width: 480px) {
  .footer-content {
    grid-template-columns: 1fr;
    gap: 20px;
  }
}
</style>
